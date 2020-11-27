from .PortfolioMappingStrategyMixinSQL import PortfolioMappingStrategyMixinSQL
from DataHelper.CSVtoSQL.MakeDatabaseSQL import MakeDatabaseSQL

class PortfolioMappingStrategySQL(MakeDatabaseSQL, PortfolioMappingStrategyMixinSQL):
    def __init__(self, secrets_dir=None, username=None, password=None):
        super().__init__()
        self.setup_connection(secrets_dir, username, password)
        self.setup_table_templates()
        self.setup_tables()
        self.setup_port_table_templates()
        self.setup_portfolio_tables()