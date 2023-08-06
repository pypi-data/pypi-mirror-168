# pylint: disable=duplicate-code

""" The COTA Cluster """
from typing import Dict, List

from kubernetes import client

from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (ClusterInstanceGPUConfiguration, ClusterInstances,
                                                        LocalClusterInstances)
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.serverside.job.mcli_job import MCLIVolume
from mcli.utils.utils_kube_labels import label

rtx3080_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.RTX3080,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.NODE_CLASS: label.mosaic.instance_size_types.MML_NV3080},
    cpus=128,
    cpus_per_gpu=16,
    memory=512,
    memory_per_gpu=64,
    storage=400,
    storage_per_gpu=50,
)
rtx3090_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.RTX3090,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.NODE_CLASS: label.mosaic.instance_size_types.MML_NV3090},
    cpus=128,
    cpus_per_gpu=16,
    memory=512,
    memory_per_gpu=64,
    storage=400,
    storage_per_gpu=50,
)
COTA_INSTANCES = LocalClusterInstances(gpu_configurations=[
    rtx3080_config,
    rtx3090_config,
])


class COTACluster(GenericK8sCluster):
    """ The COTA Cluster """

    allowed_instances: ClusterInstances = COTA_INSTANCES

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='local',
                    host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='local',
                    mount_path='/localdisk',
                ),
            ))

        return volumes

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        tolerations = []
        if instance_type.gpu_num > 0:
            tolerations.append({
                'effect': 'PreferNoSchedule',
                'key': label.mosaic.cota.PREFER_GPU_WORKLOADS,
                'operator': 'Equal',
                'value': 'true'
            })

        if instance_type.gpu_num == 8:
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.cota.MULTIGPU_8,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations
