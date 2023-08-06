""" The AWS Cluster """

from typing import List

from kubernetes import client

from mcli.serverside.clusters import ClusterInstances
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_pv_setup import CSIVolume, PVDetails, PVSetupMixin
from mcli.serverside.clusters.overrides.aws_instances import AWS_ALLOWED_INSTANCES
from mcli.serverside.job.mcli_k8s_job import MCLIVolume

USER_WORKDISK_STORAGE_CAPACITY: str = '5Gi'
CSI_DRIVER: str = 'efs.csi.aws.com'
CSI_VOLUME_HANDLE: str = 'fs-5cb37458'


class AWSCluster(PVSetupMixin, GenericK8sCluster):
    """ The AWS Cluster """

    allowed_instances: ClusterInstances = AWS_ALLOWED_INSTANCES
    storage_capacity: str = USER_WORKDISK_STORAGE_CAPACITY

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='workdisk',
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=f'pvc-aws-{self.mcli_cluster.namespace}'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='workdisk',
                    mount_path='/mnt/aws',
                ),
            ))
        return volumes

    @property
    def pv_name(self) -> str:
        return f'pv-aws-{self.mcli_cluster.namespace}'

    @property
    def pvc_name(self) -> str:
        return f'pvc-aws-{self.mcli_cluster.namespace}'

    def get_volume_details(self) -> PVDetails:
        """Returns the details of the PV spec
        """
        csi_details = CSIVolume(CSI_DRIVER, CSI_VOLUME_HANDLE)
        return PVDetails(csi=csi_details)

    def setup(self) -> bool:
        """Setup the cluster for future use.

        Raises:
            ClusterSetupError: Raised if setup failure prevents use of the cluster
        """
        if not self.setup_pv(self.mcli_cluster):
            return False
        return True
