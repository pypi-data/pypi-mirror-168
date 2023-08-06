""" mcli create secret Entrypoint """
import argparse
import logging
import textwrap
from typing import Callable, Optional

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.secrets import create_secret as api_create_secret
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models import MCLICluster, Secret, SecretType
from mcli.objects.secrets.cluster_secret import ClusterSecret, SecretManager
from mcli.objects.secrets.create.docker_registry import DockerSecretCreator
from mcli.objects.secrets.create.generic import EnvVarSecretCreator, FileSecretCreator
from mcli.objects.secrets.create.s3 import S3SecretCreator
from mcli.objects.secrets.create.ssh import SSHSecretCreator
from mcli.utils.utils_interactive import InputDisabledError, ValidationError, input_disabled
from mcli.utils.utils_logging import FAIL, OK, console

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete secret. Please provide the full set of arguments if running with '
                          '`--no-input`. Check `mcli create secret --help` for more information.')

CREATORS = {
    SecretType.docker_registry: DockerSecretCreator,
    SecretType.environment: EnvVarSecretCreator,
    SecretType.mounted: FileSecretCreator,
    SecretType.ssh: SSHSecretCreator,
    SecretType.git: SSHSecretCreator,
    SecretType.sftp: SSHSecretCreator,
    SecretType.s3: S3SecretCreator,
}


def create_new_secret(
    secret_type: SecretType,
    secret_name: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    kwargs.pop('func', None)

    with input_disabled(no_input):
        try:
            creator = CREATORS[secret_type]()
            secret = creator.create(name=secret_name, **kwargs)

            conf: MCLIConfig = MCLIConfig.load_config()
            if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
                with console.status('Creating secrets..'):
                    api_create_secret(secret=secret, timeout=None)
            else:
                sync_secret(secret)

            logger.info(f'{OK} Created {secret.secret_type} secret: {secret.name}')
        except (KubernetesException, MAPIException) as e:
            logger.error(f'{FAIL} {e}')
            return 1
        except RuntimeError as e:
            logger.error(f'{FAIL} {e}')
            return 1
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except ValidationError as e:
            logger.error(f'{FAIL} {e}')
            return 1

    return 0


def copy_existing_secret(
    secret_name: str,
    cluster_name: str,
    namespace: str,
    **kwargs,
):
    """Copy an existing secret to the user's clusters

    Args:
        secret_name: Name of secret in a shared namespace
        cluster_name: Name of the cluster in which the secret is stored
        namespace: Namespace in which the shared secret lives
    """
    del kwargs

    try:

        conf = MCLIConfig.load_config()

        # Check that the cluster exists
        mcli_cluster: Optional[MCLICluster] = None
        for pl in conf.clusters:
            if pl.name == cluster_name:
                mcli_cluster = pl
                break

        if mcli_cluster is None:
            cluster_names = {pl.name for pl in conf.clusters}
            raise ValueError(
                f'Invalid cluster: Cluster must be one of {sorted(list(cluster_names))}. Got: {cluster_name}')

        # Get available secrets from new cluster
        manager = SecretManager(
            MCLICluster(name=cluster_name, kubernetes_context=mcli_cluster.kubernetes_context, namespace=namespace))
        available_secrets = manager.get_secrets()
        logger.debug(f'Found {len(available_secrets)} secrets in cluster {cluster_name}')

        # Check if secret exists
        new_secret: Optional[Secret] = None
        for cluster_secret in available_secrets:
            if cluster_secret.secret.name == secret_name:
                new_secret = cluster_secret.secret
                break

        if new_secret is None:
            raise ValueError(
                f'Secret not found: Could not find secret {secret_name} in {namespace} namespace of cluster '
                f'{cluster_name}. Please double-check these values.')

        # Sync secret to user's clusters
        logger.info(f'{OK} Copying existing secret: {secret_name}')
        sync_secret(new_secret)
        logger.info(f'{OK} Synced to all clusters')
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except ValueError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    return 0


def sync_secret(secret: Secret):
    conf = MCLIConfig.load_config()

    # Sync to all known clusters
    cluster_secret = ClusterSecret(secret)
    with console.status('Creating secret in all cluster...') as status:
        for cluster in conf.clusters:
            with MCLICluster.use(cluster):
                status.update(f'Creating secret in cluster: {cluster.name}...')
                cluster_secret.create(cluster.namespace)


def _add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--name',
        dest='secret_name',
        metavar='NAME',
        help='What you would like to call the secret. Must be unique',
    )
    parser.add_argument('--no-input', action='store_true', help='Do not query for user input')


def _add_docker_registry_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    DOCKER_EXAMPLES = """

    Examples:

    # Add docker credentials interactively
    mcli create secret docker

    # Add credentials for a custom docker registry
    mcli create secret --username my-user --password my-registry-key --server https://custom-registry.com
    """
    docker_registry_parser = subparser.add_parser(
        'docker',
        help='Create a secret to let you pull images from a private Docker registry.',
        description='Create a secret to let you pull images from a private Docker registry.',
        epilog=DOCKER_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(docker_registry_parser)
    docker_registry_parser.add_argument(
        '--username',
        dest='username',
        help='Your username for the Docker registry',
    )
    docker_registry_parser.add_argument(
        '--password',
        dest='password',
        help='Your password for the Docker registry. If possible, use an API key here.',
    )
    docker_registry_parser.add_argument(
        '--email',
        dest='email',
        help='The email you use for the Docker registry',
    )
    docker_registry_parser.add_argument('--server',
                                        dest='server',
                                        help='The URL for the Docker registry. '
                                        'For DockerHub, this should be https://index.docker.io/v1/.')
    docker_registry_parser.set_defaults(func=secret_handler, secret_type=SecretType.docker_registry)
    return docker_registry_parser


def _add_ssh_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add an SSH key
    mcli create secret ssh ~/.ssh/my_id_rsa

    # Give the secret a special name and special mount point
    mcli create secret ssh ~/.ssh/my_id_rsa --name my-ssh-key --mount-path /secrets/foo

    # Add an SSH secret interactively
    mcli create secret ssh
    """
    ssh_parser = subparser.add_parser(
        'ssh',
        help='Create an SSH secret for your SSH private key',
        description='Add your SSH private key to mcli to enable SSH from within your workloads. '
        'This allows you to get data into your workloads via SSH, for example from an SFTP server.',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ssh_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path the private key of an SSH key-pair')
    ssh_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(ssh_parser)
    ssh_parser.set_defaults(func=secret_handler, secret_type=SecretType.ssh, git=False)


def _add_git_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add a Git SSH key
    mcli create secret git-ssh ~/.ssh/github_id_rsa

    # Give the secret a special name and special mount point
    mcli create secret git-ssh ~/.ssh/github_id_rsa --name my-git-key --mount-path /secrets/foo

    # Add a Git SSH secret interactively
    mcli create secret git-ssh
    """
    git_parser = subparser.add_parser(
        'git-ssh',
        help='Create an SSH secret for use with Git commands',
        description='Add an SSH private key to your workloads to access private Git repos over SSH. '
        'To use this, you\'ll also need to register the associated public SSH key to your account '
        'at github.com (or your repository host of choice).',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    git_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path to the private key of an SSH key-pair')
    git_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(git_parser)
    git_parser.set_defaults(func=secret_handler, secret_type=SecretType.git, git=True)


def _add_sftp_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add an SFTP key
    mcli create secret sftp-ssh ~/.ssh/sftp_id_rsa

    # Give the secret a special name and special mount point
    mcli create secret sftp-ssh ~/.ssh/sftp_id_rsa --name my-sftp-key --mount-path /secrets/foo

    # Add an SFTP SSH secret interactively
    mcli create secret sftp-ssh
    """
    sftp_parser = subparser.add_parser(
        'sftp-ssh',
        help='Create an SSH secret for use with SFTP',
        description='Add an SSH private key to your workloads to access an SFTP server over SSH.',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sftp_parser.add_argument('ssh_private_key',
                             metavar='</path/to/private-key>',
                             nargs='?',
                             help='Path to the private key of an SSH key-pair')
    sftp_parser.add_argument('--mount-path',
                             metavar='</path/inside/workload>',
                             help='Location in your workload at which the SSH key should be mounted')
    sftp_parser.add_argument('--host-name', help='The hostname of the sftp server.')
    sftp_parser.add_argument('--no-host-check',
                             action='store_true',
                             default=False,
                             help='Do not verify fingerprints before adding SSH hosts to known_hosts. '
                             'WARNING: Disabling host checking is a security risk use with caution.')
    _add_common_arguments(sftp_parser)
    sftp_parser.set_defaults(func=secret_handler, secret_type=SecretType.sftp, sftp=True)


def _add_mounted_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = textwrap.dedent("""

    Examples:

    # Add a file-mounted secret interactively
    mcli create secret mounted

    # Add a secret credentials file as a mounted file secret
    mcli create secret mounted /path/to/my-credentials

    # Specify a custom secret name
    mcli create secret mounted /path/to/my-credentials --name my-file
    """)
    generic_mounted_parser = subparser.add_parser(
        'mounted',
        help='Create a secret that will be mounted as a text file',
        description='Add a confidential text file to your workloads. File-mounted secrets are '
        'more secure than env secrets because they are less likely to be leaked by the processes running in your '
        'workload (e.g. some loggers can optionally record the system environment variables to aid in '
        'reproducibility).',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generic_mounted_parser.add_argument('secret_path',
                                        nargs='?',
                                        metavar='</path/to/secret/file>',
                                        help='A text file with secret data that you\'d like '
                                        'to have mounted within your workloads.')
    generic_mounted_parser.add_argument('--mount-path',
                                        metavar='</path/inside/workload>',
                                        help='Location in your workload at which the secret should be mounted. '
                                        'The file will be mounted at <mount-path>/secret. Must be unique')
    _add_common_arguments(generic_mounted_parser)
    generic_mounted_parser.set_defaults(func=secret_handler, secret_type=SecretType.mounted)


def _add_env_var_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add a secret API key as an environment variable named FOO
    mcli create secret env FOO=super-secret-api-key-1234

    # Give the secret a special name
    mcli create secret env FOO=super-secret-api-key-1234 --name my-env-var

    # Add an environment variable secret interactively
    mcli create secret env
    """
    generic_env_parser = subparser.add_parser(
        'env',
        help='Create a secret that will be exposed as an environment variable',
        description='Create a secret that will be exposed as an environment variable. This lets you easily use '
        'arbitrary confidential information within your workloads.',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generic_env_parser.add_argument(
        'env_pair',
        nargs='?',
        help='A KEY=VALUE pair',
    )
    _add_common_arguments(generic_env_parser)
    generic_env_parser.set_defaults(func=secret_handler, secret_type=SecretType.environment)


def _add_s3_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    DESCRIPTION = """
Add your S3 config file and credentials file to MCLI for use in your workloads.

Your config and credentials files should follow the standard structure output
by `aws configure`:

~/.aws/config:

[default]
region=us-west-2
output=json


~/.aws/credentials:

[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY


More details on these files can be found here:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

Once you've created an S3 secret, MCLI will automatically mount it to your workloads
and export two environment variables:

$AWS_CONFIG_FILE:             Path to your config file
$AWS_SHARED_CREDENTIALS_FILE: Path to your credentials file

Most s3-compliant libraries will use these environment variables to discover your
credentials by default.
    """

    # pylint: disable-next=invalid-name
    EXAMPLES = """

Examples:

# Add your s3 secret interactively
> mcli create secret s3
? What would you like to name this secret? my-s3-credentials
? Where is your S3 config file located? ~/.aws/config
? Where is your S3 credentials file located? ~/.aws/credentials
✔  Created secret: my-s3-credentials
✔  Synced to all clusters

# Add your s3 secret using arguments
> mcli create secret s3 --name my-s3-credentials --config-file ~/.aws/config --credentials-file ~/.aws/credentials

    """
    s3_cred_parser = subparser.add_parser(
        's3',
        help='Add your S3 config and credentials to MCLI',
        description=DESCRIPTION,
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(s3_cred_parser)
    s3_cred_parser.add_argument('--config-file',
                                metavar='PATH',
                                help='Path to your S3 config file. Usually `~/.aws/config`')
    s3_cred_parser.add_argument('--credentials-file',
                                metavar='PATH',
                                help='Path to your S3 credentials file. Usually `~/.aws/credentials`')
    s3_cred_parser.add_argument(
        '--mount-directory',
        metavar='PATH',
        help='Location in your workload at which your credentials and config files will be mounted')
    s3_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.s3)


def _add_shared_subparser(subparser: argparse._SubParsersAction,):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add a shared s3 secret from the rxzx cluster
    mcli create secret shared --name streaming-credentials-s3 --cluster rxzx --namespace shared-namespace
    """

    shared_parser = subparser.add_parser(
        'shared',
        help='Copy an existing secret from a shared store',
        description='',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    shared_parser.add_argument('--name',
                               dest='secret_name',
                               required=True,
                               help='Name of an existing secret',
                               metavar='NAME')

    conf = MCLIConfig.load_config(safe=True)
    cluster_names = sorted([pl.name for pl in conf.clusters])
    shared_parser.add_argument(
        '--cluster',
        '--platform',
        dest='cluster_name',
        required=True,
        choices=cluster_names,
        metavar='CLUSTER',
        help=f'Name of the cluster that contains the secret. Choices: {", ".join(cluster_names)}')

    shared_parser.add_argument('--namespace', required=True, help='Namespace that contains the secret')
    shared_parser.set_defaults(func=copy_existing_secret)


def configure_secret_argparser(
    parser: argparse.ArgumentParser,
    secret_handler: Callable,
) -> None:

    subparser = parser.add_subparsers(title='MCLI Secrets',
                                      description='The table below shows the types of secrets that you can create',
                                      help='DESCRIPTION',
                                      metavar='SECRET_TYPE')

    # Environment variables
    _add_env_var_subparser(subparser, secret_handler)

    # Mounted secrets
    _add_mounted_subparser(subparser, secret_handler)

    # Docker registry
    _add_docker_registry_subparser(subparser, secret_handler)

    # SSH credentials
    _add_ssh_subparser(subparser, secret_handler)

    # Git credentials
    _add_git_subparser(subparser, secret_handler)

    # SFTP credentials
    _add_sftp_subparser(subparser, secret_handler)

    # S3 credentials
    _add_s3_subparser(subparser, secret_handler)

    # Shared secret
    _add_shared_subparser(subparser)
