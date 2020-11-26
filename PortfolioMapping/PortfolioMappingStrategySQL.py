from .PortfolioMappingStrategyMixinSQL import PortfolioMappingStrategyMixinSQL
from DataHelper.CSVtoSQL.MakeDatabaseSQL import MakeDatabaseSQL

class PortfolioMappingStrategySQL(MakeDatabaseSQL, PortfolioMappingStrategyMixinSQL):
    def __init__(self, username='fx_admin', password = '#Flexstone2020'):
        secrets_dir = '/Users/twx'
        super().__init__(secrets_dir, username, password)
        self.setup_connection(secrets_dir, username, password)
        self.setup_table_templates()
        self.setup_tables()
        self.setup_port_table_templates()
        self.setup_portfolio_tables()