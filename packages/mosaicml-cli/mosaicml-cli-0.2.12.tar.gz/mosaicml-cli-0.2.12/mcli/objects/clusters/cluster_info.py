"""Helpers for cluster info"""
from typing import List

from mcli.config import MCLIConfig
from mcli.models import MCLICluster


def get_cluster_list() -> List[MCLICluster]:
    conf = MCLIConfig.load_config()
    return conf.clusters
