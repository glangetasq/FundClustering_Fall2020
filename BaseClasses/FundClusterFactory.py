from .StrategyFactory import StrategyFactory

CLUSTER_CLASS_CONFIG = {} #{Fund_cluster_method_name(str): derived class of FundClusterBased(class)}
CLUSTER_VISUALIZER_CLASS_CONFIG = {} # {Fund_cluster_method_name(str): derived class of FundClusterVisualizationHelperBased(class)}


class FundClusterFactory(StrategyFactory):
    """Factory to generate clustering strategy obj and visualizer obj"""
    
    def __init__(self):
        super().__init__(CLUSTER_CLASS_CONFIG, CLUSTER_VISUALIZER_CLASS_CONFIG)
