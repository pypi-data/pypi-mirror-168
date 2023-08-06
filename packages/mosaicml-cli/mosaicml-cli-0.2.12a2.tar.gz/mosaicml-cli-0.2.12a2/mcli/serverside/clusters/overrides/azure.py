# pylint: disable=duplicate-code

""" The Azure Cluster """

from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import ClusterInstances


class AzureCluster(GenericK8sCluster):
    """ The Azure Cluster """

    allowed_instances: ClusterInstances = ClusterInstances()
