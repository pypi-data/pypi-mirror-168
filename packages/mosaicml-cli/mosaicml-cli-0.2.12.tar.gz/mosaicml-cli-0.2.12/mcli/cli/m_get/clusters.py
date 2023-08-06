"""CLI getter for clusters"""
from dataclasses import dataclass
from typing import Dict, Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.models import MCLICluster
from mcli.serverside.clusters.cluster_instances import UserInstanceRegistry
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_logging import FAIL, err_console


@dataclass
class ClusterDisplayItem(MCLIDisplayItem):
    name: str
    context: str
    namespace: str
    gpu_types_and_nums: Dict[str, List[int]]


class MCLIClusterDisplay(MCLIGetDisplay):
    """`mcli get cluster` display class
    """

    def __init__(self, cluster: List[MCLICluster]):
        self.cluster = cluster

    def __iter__(self) -> Generator[ClusterDisplayItem, None, None]:
        gpu_registry = _get_gpu_registry(self.cluster)
        for cluster in self.cluster:
            yield ClusterDisplayItem(name=cluster.name,
                                     context=cluster.kubernetes_context,
                                     namespace=cluster.namespace,
                                     gpu_types_and_nums=gpu_registry[cluster.name])


def _get_gpu_registry(clusters: List[MCLICluster]) -> Dict[str, Dict[str, List[int]]]:
    user_registry = UserInstanceRegistry(clusters=clusters)
    gpu_info: Dict[str, Dict[str, List[int]]] = {}
    for cluster, gpu_dict in user_registry.registry.items():
        gpu_info[cluster] = {}
        for gpu_type, gpu_nums in gpu_dict.items():
            if gpu_type == GPUType.NONE:
                gpu_type_str = 'none (CPU only)'
            else:
                gpu_type_str = gpu_type.value
            gpu_info[cluster][gpu_type_str] = gpu_nums
    return gpu_info


def get_clusters(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. Please run `mcli init` and then `mcli create cluster` '
                          'to create your first cluster.')
        return 1

    display = MCLIClusterDisplay(conf.clusters)
    display.print(output)
    return 0
