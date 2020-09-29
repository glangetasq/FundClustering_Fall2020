class StrategyFactory:
    """Factory that could be used to generate a strategy and visualier of the it.
    Please do not touch this class unless you find some bug, do the adjustment on FundClusterFactory"""

    def __init__(self, strategy_class_config, visualizer_class_config):
        self._strategy = {}
        self._visualizers = {}
        self._strategy_class_config = strategy_class_config
        self._visualizer_class_config = visualizer_class_config
    
    def register_cluster(self, strategy_name):
        """Function to register an strategy in the factory, avaialble alloator could be found in self._strategy_class_config
            Later this could be implemented to load cached allocator and visualizer from Pickle directly too
        Parameters:
            strategy_name: str
                represent the strategy that we want to register
        """
        if cluster_name not in self._strategy_class_config:
            raise ValueError(f'{strategy_name} Strategy Class could not be found in configuration')
        if  strategy_name not in self._visualizer_class_config: 
            raise ValueError(f'{strategy_name} Visualizer Class could not be found in configuration')

        self._strategy[strategy_name] = self._strategy_class_config[strategy_name](strategy_name)
        self._visualizer[strategy_name] = self._visualizer_class_config[strategy_name](self._allocator[strategy_name])
    
    def create_strategy(self, strategy_name):
        """Function to load the strategy from the factory center
        Parameters:
            strategy_name: str
                represent the allocator that we want to register
        """
        strategy = self._strategy.get(strategy_name)
        if allocator is None:
            raise ValueError(f'{strategy_name} Allocator has not been registered, please register before using it')
        return allocator
    
    def create_visualizer(self, strategy_name):
        """Function to load the visualizer from the factory center
        Parameters:
            strategy_name: str
                represent the allocator that we want to register
        """
        visualizer = self._visualizer.get(strategy_name)
        if visualizer is None:
            raise ValueError(f'{strategy_name} Visualizer has not been registered, please register before using it')
        return visualizer
