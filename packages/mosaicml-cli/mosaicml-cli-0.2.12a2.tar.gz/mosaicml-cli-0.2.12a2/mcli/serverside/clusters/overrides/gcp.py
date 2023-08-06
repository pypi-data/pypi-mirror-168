# pylint: disable=duplicate-code

""" The GCP Cluster """

from typing import Dict, List

from kubernetes import client

from mcli.models.mcli_cluster import MCLICluster
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import ClusterInstances
from mcli.serverside.clusters.cluster_pv_setup import NFSVolume, PVDetails, PVSetupMixin
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.serverside.clusters.overrides.gcp_instances import GCP_ALLOWED_INSTANCES
from mcli.serverside.clusters.overrides.r1z2 import (USER_WORKDISK_PATH, USER_WORKDISK_SERVER,
                                                     USER_WORKDISK_STORAGE_CAPACITY)
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.utils.utils_kube_labels import label

USER_WORKDISK_STORAGE_CAPACITY = '5Gi'
USER_WORKDISK_PATH = '/rancher'
USER_WORKDISK_SERVER = '10.173.118.250'


class GCPCluster(PVSetupMixin, GenericK8sCluster):
    """ The GCP Cluster """

    allowed_instances: ClusterInstances = GCP_ALLOWED_INSTANCES
    storage_capacity: str = USER_WORKDISK_STORAGE_CAPACITY

    def __init__(self, mcli_cluster: MCLICluster) -> None:
        super().__init__(mcli_cluster)
        self.interactive = True

    def get_annotations(self, instance_type: InstanceType) -> Dict[str, str]:
        annotations = super().get_annotations(instance_type)
        if instance_type.gpu_type in (GPUType.TPUv2, GPUType.TPUv3):
            annotations[label.gcp.TPU_ANNOTATION] = label.gcp.TF_VERSION
        return annotations

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='workdisk',
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=f'pvc-gcp-{self.mcli_cluster.namespace}'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='workdisk',
                    mount_path='/mnt/gcp',
                ),
            ))

        return volumes

    @property
    def pv_name(self) -> str:
        return f'pv-gcp-{self.mcli_cluster.namespace}'

    @property
    def pvc_name(self) -> str:
        return f'pvc-gcp-{self.mcli_cluster.namespace}'

    def get_volume_details(self) -> PVDetails:
        """Returns the details of the PV spec
        """
        nfs_details = NFSVolume(USER_WORKDISK_PATH, USER_WORKDISK_SERVER)
        return PVDetails(nfs=nfs_details)

    def setup(self) -> bool:
        """Setup the cluster for future use.

        Raises:
            ClusterSetupError: Raised if setup failure prevents use of the cluster
        """
        if not self.setup_pv(self.mcli_cluster):
            return False
        return True
