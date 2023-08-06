""" mcli interactive Entrypoint """
import argparse
import logging
from typing import Optional, Set

from mcli.api.exceptions import MCLIRunConfigValidationError
from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models.mcli_cluster import MCLICluster
from mcli.models.run_config import FinalRunConfig, RunConfig
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (IncompleteInstanceRequest, InstanceRequest,
                                                        InstanceTypeUnavailable, UserInstanceRegistry, ValidInstance)
from mcli.serverside.clusters.instance_type import GPUType
from mcli.serverside.job.mcli_job import MCLIJob, MCLIJobType
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import ClusterRun, connect_to_pod, delete_runs
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_run_status import PodStatus, RunStatus
from mcli.utils.utils_types import get_hours_type

_MAX_INTERACTIVE_DURATION: float = 12

logger = logging.getLogger(__name__)


def _get_interactive_instance_registry() -> UserInstanceRegistry:

    interactive_clusters = []
    for cluster in MCLIConfig.load_config(safe=True).clusters:
        if GenericK8sCluster.from_mcli_cluster(cluster).interactive:
            interactive_clusters.append(cluster)

    return UserInstanceRegistry(interactive_clusters)


# pylint: disable-next=invalid-name
INTERACTIVE_REGISTRY = _get_interactive_instance_registry()


def interactive_entrypoint(
    name: Optional[str] = None,
    cluster: Optional[str] = None,
    gpu_type: Optional[str] = None,
    gpus: Optional[int] = None,
    cpus: int = 1,
    hours: float = 1,
    image: str = 'mosaicml/pytorch',
    confirm: bool = True,
    connect: bool = True,
    **kwargs,
) -> int:
    del kwargs

    try:
        request = InstanceRequest(cluster=cluster, gpu_type=gpu_type, gpu_num=gpus)
        options = INTERACTIVE_REGISTRY.lookup(request)
        logger.debug(f'Found {len(options)} potential instances')

        valid_instance: Optional[ValidInstance] = None
        if len(options) == 1:
            valid_instance = options[0]
        elif len(options) > 1:
            # If multiple options, check for r1z2 options and choose the one with the fewest GPUs
            r1z2_options = [option for option in options if option.cluster == 'r1z2']
            if r1z2_options:
                valid_instance = sorted(r1z2_options, key=lambda x: x.gpu_num)[0]

        if not valid_instance:
            raise IncompleteInstanceRequest(request, ValidInstance.to_registry(options), INTERACTIVE_REGISTRY.registry)
        logger.debug(f'Chosen instance type: {valid_instance}')

        if not name:
            name = f'interactive-{valid_instance.gpu_type.replace("_", "-")}-{valid_instance.gpu_num}'.lower()

        partial_run = RunConfig(
            run_name=name,
            cluster=valid_instance.cluster,
            gpu_type=valid_instance.gpu_type,
            gpu_num=valid_instance.gpu_num,
            cpus=cpus,
            optimization_level=0,
            command=f'sleep {int(3600 * hours)}',
            image=image,
        )
        final_config = FinalRunConfig.finalize_config(partial_run)

        mcli_job = MCLIJob.from_final_run_config(run_config=final_config)

        if valid_instance.gpu_type != str(GPUType.NONE):
            gpu_cpu_string = f'{valid_instance.gpu_num} GPU(s)'
        else:
            gpu_cpu_string = f'{cpus} CPU(s)'

        logger.info(
            f'{OK} Ready to submit a [bold]{gpu_cpu_string}[/] interactive session for [bold]{hours} hour(s)[/] '
            f'to cluster [bold green]{valid_instance.cluster}[/]')
        if confirm:
            confirm = query_yes_no('Do you want to submit?')
            if not confirm:
                raise RuntimeError('Canceling!')

        mcli_cluster = MCLICluster.get_by_name(valid_instance.cluster)
        # We already know this is a valid cluster name, so it should never return None
        assert mcli_cluster is not None
        exit_code = run_mcli_job_interactively(mcli_job, mcli_cluster, connect)
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except (InstanceTypeUnavailable) as e:
        logger.error(e)
        return 1
    except (MCLIRunConfigValidationError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(e)
        return 1

    return exit_code or 0


def run_mcli_job_interactively(
    mcli_job: MCLIJob,
    mcli_cluster: MCLICluster,
    connect: bool,
) -> int:
    runner = Runner()
    runner.submit(job=mcli_job, job_type=MCLIJobType.INTERACTIVE)

    context = mcli_cluster.to_kube_context()
    exec_cmd = f'kubectl --context {context.name} exec -it job/{mcli_job.unique_name} -- /bin/bash'

    if connect:
        with MCLICluster.use(mcli_cluster):
            logger.info(f'{INFO} Interactive session submitted. Waiting for it to start...')
            logger.info(f'{INFO} Press Ctrl+C to quit and interact with your session manually.')
            epilog = RunEpilog(mcli_job.unique_name, mcli_cluster.namespace)
            last_status: Optional[PodStatus] = None
            with EpilogSpinner() as spinner:
                last_status = epilog.wait_until(callback=spinner, timeout=300)

            # Wait timed out
            common_log = CommonLog(logger)
            if last_status is None:
                get_pods_cmd = f'kubectl --context {context.name} get pods -w {epilog.rank0_pod}'
                logger.warning(
                    'Waiting for interactive session to spawn exceeded the timeout. You can monitor it '
                    f'using:\n\n{get_pods_cmd}\n\n'
                    f'Once the pod is "Running", you can attach to it using:\n\n{exec_cmd}',)
                return 0
            elif last_status.state == RunStatus.FAILED_PULL:
                common_log.log_pod_failed_pull(mcli_job.unique_name, mcli_job.image)
                with console.status('Deleting failed run...'):
                    delete_runs([ClusterRun(mcli_job.unique_name, mcli_cluster.to_kube_context())])
                return 1
            elif last_status.state == RunStatus.FAILED:
                common_log.log_pod_failed(mcli_job.unique_name)
                return 1
            elif last_status.state.before(RunStatus.RUNNING):
                common_log.log_unknown_did_not_start()
                logger.debug(last_status)
                return 1

            logger.info(f'{OK} Interactive session created. Attaching...')
            logger.info(
                f'{INFO} Press Ctrl+C to quit attaching. Once attached, press Ctrl+D or type exit '
                'to leave the session.',)
            connected = connect_to_pod(epilog.rank0_pod, context)
            if not connected:
                logger.warning(f'{FAIL} Could not connect to the interactive session.')
                logger.warning(
                    f'Please double-check that [bold]{context.name}[/] is your context and '
                    f'[bold]{context.namespace}[/] is your correct namespace.',)
                logger.warning(f'If so, try manually running {exec_cmd}')
    else:
        logger.info(f'{OK} Interactive session submitted. You can connect using:\n\n{exec_cmd}')
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:

    parser.add_argument(
        '--name',
        default=None,
        type=str,
        help='Name for the interactive session. '
        'Default: "interactive-<gpu type>-<gpu num>"',
    )

    if INTERACTIVE_REGISTRY.registry:
        cluster_descriptions = [
            IncompleteInstanceRequest.get_cluster_description(pl, instances)
            for pl, instances in INTERACTIVE_REGISTRY.registry.items()
        ]
        full_cluster_description = '\nAvailable interactive instances:\n\n'
        full_cluster_description += '\n'.join(cluster_descriptions)
    else:
        full_cluster_description = '\nNo interactive instances available\n\n'

    cluster_arguments = parser.add_argument_group('Instance settings', description=full_cluster_description)
    available_clusters = sorted(list(INTERACTIVE_REGISTRY.registry.keys()))
    cluster_arguments.add_argument(
        '--cluster',
        '--platform',
        default=None,
        choices=available_clusters,
        metavar='CLUSTER',
        help='Cluster where your interactive session should run. If you '
        'only have one available, that one will be selected by default. '
        'Depending on your cluster, you\'ll have access to different GPU types and counts. '
        'See the available combinations above. '
        f'Choices: {", ".join(available_clusters)}',
    )

    available_types: Set[str] = set()
    available_nums: Set[int] = set()
    for instance in INTERACTIVE_REGISTRY.registry.values():
        for gpu_type, gpu_nums in instance.items():
            available_types.add(str(gpu_type))
            available_nums.update(set(gpu_nums))
    gpu_types = sorted(list(available_types))
    gpu_nums = sorted(list(available_nums))

    cluster_arguments.add_argument(
        '--gpu-type',
        choices=gpu_types,
        metavar='TYPE',
        help=f'Type of GPU to use. Choices: {", ".join(gpu_types)}. '
        'Valid GPU types depend on the cluster and GPU numbers requested. See the available combinations above',
    )
    cluster_arguments.add_argument(
        '--gpus',
        type=int,
        metavar='NGPUs',
        choices=gpu_nums,
        help=f'Number of GPUs to run interactively. Choices: {", ".join(str(x) for x in gpu_nums)}. '
        'Valid GPU numbers depend on the cluster and GPU type. See the available combinations above.',
    )
    cluster_arguments.add_argument(
        '--cpus',
        default=1,
        type=int,
        metavar='NCPUs',
        help='Number of CPUs to run interactively. This will only take effect when --gpu-type is set to "none". '
        'Default: %(default)s',
    )

    parser.add_argument(
        '--hours',
        default=1,
        type=get_hours_type(_MAX_INTERACTIVE_DURATION),
        help='Number of hours the interactive session should run. '
        f' Default: %(default)s. MAX: {_MAX_INTERACTIVE_DURATION}',
    )
    parser.add_argument(
        '--image',
        default='mosaicml/pytorch',
        help='Docker image to use',
    )
    parser.add_argument(
        '-y',
        '--no-confirm',
        dest='confirm',
        action='store_false',
        help='Do not request confirmation',
    )
    parser.add_argument(
        '--no-connect',
        dest='connect',
        action='store_false',
        help='Do not connect to the interactive session immediately',
    )

    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        help='Create an interactive session',
        description=('Create an interactive session on a node with persistent storage. '
                     'Once created, you can attach to the session. '
                     'Interactive sessions are only allowed in pre-specified clusters.'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
