from .PortfolioMappingStrategyMixinSQL import PortfolioMappingStrategyMixinSQL

class PortfolioMappingStrategySQL(PortfolioMappingStrategyMixinSQL)
    def __init__(self, username, password):
        super().__init__()
        self.setup_connection(username, password)
        self.setup_table_templates()
        self.setup_tables()
        self.setup_port_table_templates()
        self.setup_portfolio_tables()