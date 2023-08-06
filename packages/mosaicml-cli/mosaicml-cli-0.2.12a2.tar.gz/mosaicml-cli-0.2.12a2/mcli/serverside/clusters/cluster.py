# pylint: disable=duplicate-code

""" The base class for how a cluster will operate """
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

from kubernetes import client

from mcli.models import MCLICluster
from mcli.objects.secrets.cluster_secret import SecretManager
from mcli.serverside.clusters.cluster_instances import ClusterInstances
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.serverside.job.mcli_k8s_resource_requirements_typing import MCLIK8sResourceRequirements
from mcli.utils.utils_kube import safe_update_optional_dictionary, safe_update_optional_list

if TYPE_CHECKING:
    from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob, MCLIVolume
# types
Resources = Dict[str, int]
Description = Dict[str, Any]


class PriorityLabel(Enum):
    """Enum to specify the priority for a run.
    """
    low = 'low'
    standard = 'standard'
    high = 'high'

    @classmethod
    def ensure_enum(cls, val: Union[str, PriorityLabel]) -> PriorityLabel:
        if isinstance(val, PriorityLabel):
            return val
        try:
            return PriorityLabel[val]
        except KeyError:
            pass

        raise ValueError(f'Unable to ensure {val} is a PriorityLabel Enum')

    def __str__(self):
        return str(self.value)


class InvalidPriorityError(Exception):
    """Raised if an invalid priority class is requested
    """
    requested_class: str
    valid_classes: List[str]
    cluster: Optional[str]

    def __init__(self, requested_class: str, valid_classes: List[str], cluster: Optional[str] = None):
        self.requested_class = requested_class
        self.valid_classes = valid_classes
        self.cluster = cluster
        super().__init__()

    def __str__(self) -> str:
        cluster_message = f'Cluster {self.cluster + " " if self.cluster else ""}does not support'
        if self.valid_classes:
            valid_classes = ', '.join(sorted(self.valid_classes))
            error_message = (f'{cluster_message} priority class: {self.requested_class}. '
                             f'Must be one of: {valid_classes}')
        else:
            error_message = f'{cluster_message} priority classes'

        return error_message


class ClusterSetupError(Exception):
    """Raised if cluster setup failed
    """


class ClusterCreationError(Exception):
    """Raised if cluster setup failed
    """


class ClusterResourceHandler():
    """ All Instance Related Functions """
    allowed_instances: ClusterInstances

    def get_instance_type(self, gpu_type: GPUType, gpu_num: int, cpus: Optional[int] = None) -> InstanceType:
        return self.allowed_instances.get_instance_type(
            gpu_type=gpu_type,
            gpu_num=gpu_num,
            cpus=cpus,
        )


class ClusterPriorityHandler():
    # priority class to use for the job
    priority_class_labels: Dict[str, str] = {}
    default_priority_class: Optional[str] = None  # If a priority class should be default, put it here.

    def get_priority_class_label(self, priority_class_override: Optional[str]) -> Optional[str]:
        priority_class = priority_class_override if priority_class_override else self.default_priority_class
        priority_class_label: Optional[str] = None
        if priority_class is not None:
            if priority_class not in self.priority_class_labels:
                raise InvalidPriorityError(priority_class, list(self.priority_class_labels))
            priority_class_label = self.priority_class_labels[priority_class]
        return priority_class_label


class ClusterProperties():
    mcli_cluster: MCLICluster

    @property
    def namespace(self):
        return self.mcli_cluster.namespace

    @property
    def kubernetes_context(self):
        return self.mcli_cluster.kubernetes_context


class GenericK8sCluster(
        ClusterResourceHandler,
        ClusterPriorityHandler,
        ClusterProperties,
):
    """ A Generic Cluster implementation """

    interactive: bool = False
    pod_group_scheduler: Optional[str] = None

    @staticmethod
    def get_k8s_context_map() -> Dict[str, Type[GenericK8sCluster]]:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.clusters.overrides import (AWSCluster, AzureCluster, COTACluster, GCPCluster,
                                                        Microk8sCluster, R1Z1Cluster, R1Z2Cluster, R1Z4Cluster,
                                                        R4Z1Cluster, R7Z1Cluster, R7Z2Cluster, R7Z3Cluster, R7Z4Cluster,
                                                        R7Z5Cluster, R99Z1Cluster)

        # pylint: disable-next=invalid-name
        context_map: Dict[str, Type[GenericK8sCluster]] = {
            'aws-research-01': AWSCluster,
            'azure-research-01': AzureCluster,
            'gcp-research-01': GCPCluster,
            'colo-research-01': COTACluster,
            'microk8s': Microk8sCluster,
            'r1z1': R1Z1Cluster,
            'r1z2': R1Z2Cluster,
            'r1z4': R1Z4Cluster,
            'r4z1': R4Z1Cluster,
            'r7z1': R7Z1Cluster,
            'r7z2': R7Z2Cluster,
            'r7z3': R7Z3Cluster,
            'r7z4': R7Z4Cluster,
            'r7z5': R7Z5Cluster,
            'r99z1': R99Z1Cluster,
        }
        return context_map

    @classmethod
    def from_mcli_cluster(cls, mcli_cluster: MCLICluster) -> GenericK8sCluster:
        context_map = GenericK8sCluster.get_k8s_context_map()
        if mcli_cluster.kubernetes_context not in context_map:
            raise ClusterCreationError()
        k8s_cluster = context_map[mcli_cluster.kubernetes_context]
        return k8s_cluster(mcli_cluster=mcli_cluster)

    def __init__(self, mcli_cluster: MCLICluster) -> None:
        self.mcli_cluster = mcli_cluster
        self.secret_manager = SecretManager(mcli_cluster=mcli_cluster)
        self.interactive = False
        super().__init__()

    def setup(self) -> bool:
        """Setup the cluster for future use.

        This method should be implemented by any cluster that requires user-specific setup to be performed on
        MCLICluster creation. This should be idempotent, such that if the setup is already completed, this should be
        a no-op.

        Raises:
            ClusterSetupError: Raised if setup failure prevents use of the cluster
        """
        return True

    def get_annotations(self, instance_type: InstanceType) -> Dict[str, str]:
        del instance_type
        return {}

    def get_volumes(self) -> List[MCLIVolume]:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.job.mcli_k8s_job import MCLIVolume

        return [
            MCLIVolume(
                volume=client.V1Volume(
                    name='dshm',
                    empty_dir=client.V1EmptyDirVolumeSource(medium='Memory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='dshm',
                    mount_path='/dev/shm',
                ),
            ),
        ]

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        return []

    def get_selectors(self, instance_type: InstanceType) -> Dict[str, str]:
        return instance_type.selectors

    def get_resource_requirements(self, instance_type: InstanceType) -> MCLIK8sResourceRequirements:
        return instance_type.resource_requirements

    def prepare_kubernetes_job_for_cluster(
        self,
        kubernetes_job: MCLIK8sJob,
        instance_type: InstanceType,
        priority_class: Optional[str] = None,
    ) -> None:
        """Modifies a MCLIK8sJob with the proper specs of the Cluster

        Args:
            kubernetes_job: The MCLIK8sJob object to that represents the K8s job
            instance_type: The instance type to use on the cluster
            priority_class: An optional priority class to assign the job to
        """
        kubernetes_job.metadata.namespace = self.namespace
        kubernetes_job.spec.backoff_limit = 0
        kubernetes_job.pod_spec.node_selector.update(self.get_selectors(instance_type))
        kubernetes_job.pod_spec.container.resources = self.get_resource_requirements(instance_type)

        volumes = self.get_volumes()
        for volume in volumes:
            kubernetes_job.add_volume(volume)

        annotations = self.get_annotations(instance_type=instance_type)
        pts = kubernetes_job.pod_template_spec
        pts.metadata.annotations = safe_update_optional_dictionary(pts.metadata.annotations, annotations)

        pod_spec = kubernetes_job.pod_spec
        pod_spec.priority_class_name = self.get_priority_class_label(priority_class_override=priority_class)
        pod_spec.tolerations = safe_update_optional_list(pod_spec.tolerations, self.get_tolerations(instance_type))

        pod_spec.restart_policy = 'Never'
        pod_spec.host_ipc = True

        # Add secrets to job
        self.secret_manager.add_secrets_to_job(kubernetes_job=kubernetes_job)
