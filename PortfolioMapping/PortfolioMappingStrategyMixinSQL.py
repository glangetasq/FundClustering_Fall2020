import pandas as pd
import json
from BaseClasses import PortfolioMappingStrategyMixin
from DataHelper.SQLDataHandler import SQLDataHandler
from config import SQL_CONFIG

SCHEMA = SQL_CONFIG['database']


class PortfolioMappingStrategyMixinSQL(SQLDataHandler, PortfolioMappingStrategyMixin):
    """This is a class that you implement a simple python logics to do portfolio mapping, and
    Inlcude SQL Operation in Mutual Fund Performance Feature Calculation"""

    def setup_port_table_templates(self):
        """Define the all table template as local variable here, all these table template should be defined as a global variable in a
        python file, and import here for this class to use, please check the sauma.core documentation, the template format should be something like:
        {
            "tableName": "Test",
            "schema": "test_db",
            "primaryKey":["id"],
            "columns": [{"name": "id",       "type":"INTEGER"},                           // case insensitive
                        {"name": "text_col", "type":"STRING", "size":50},
                        {"name": "int_col",  "type":"INT"}
            ],
            "primaryKey":["id"],
            "description": 'sample table to know about the format'
        }


        for example, you define a list of template under performance_feature/custom.py
        so you could do from performance_feature.custom import TEMPLATE_A, TEMPLATE_B, TEMPLATE_C
        and do self.templateA = TEMPLATE_A inside this class
        and do self.look_up_or_create_table(self.templateA) to setup the table in the setup_table function
        as the sauma.core package require a json obj as input, you may need to transoform the dictionary into a json obj by doing
        import json
        # Data to be written
            dictionary ={
              "id": "04",
              "name": "sunil",
              "depatment": "HR"
            }

            # Serializing json
            json_object = json.dumps(dictionary)
        """
        TEMPLATE_PORTFOLIO = {
            "tableName": "portfolio",
            "schema": "fund_clustering",
            "columns": [{"name": "fundNo", "type": "INTEGER"},
                        {"name": "weight", "type": "FLOAT"}],
            "primaryKey": ["fundNo"],
            "description": 'fund number and weight of a portfolio'
        }

        self.template_portfolio = TEMPLATE_PORTFOLIO

    def setup_portfolio_tables(self):
        """setup all table based on the setup_table_Templates"""

        self.schema = SCHEMA
        self.conn.execute("CREATE DATABASE IF NOT EXISTS " + self.schema + ";")
        self.conn.execute('USE ' + self.schema + ';')

        self.drop_table(self.schema, "portfolio")
        self.conn.create_table(json.dumps(self.template_portfolio))

    def generate_portfolio_tmp_table(self, portfolio):
        """generate a temp table that save the portfolio information"""
        self.conn.execute('USE ' + self.schema + ';')
        self.drop_table(self.schema, "portfolio")
        self.conn.create_table(json.dumps(self.template_portfolio))
        self.conn.update_table(
            table_name='portfolio',
            schema=self.schema,
            dataframe=portfolio,
            index=False,
            if_exists='replace'
        )

    def portfolio_to_sector(self, portfolio, method='SQL'):
        """
        Given a portfolio of mutual fund, with fund name/fund id and weight on each mutual fund, map the portfolio
        to the fund cluster definition, and generate a new data framework which provide information of the mapping

        Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        and join it with a table with the cluster mapping to get the mapping"""
        if method == 'SQL':
            self.generate_portfolio_tmp_table(portfolio)
            portfolio_sector = self.conn.get_dataframe_from_sql_query("""
                SELECT p.fundNo, p.weight, c.main_cluster, c.sub_cluster
                FROM portfolio p LEFT JOIN clustering_output c ON p.fundNo=c.fundNo
                """)
        elif method == 'InMemory':
            sector_map = self.get_sector_map(method='InMemory')
            portfolio_sector = pd.merge(portfolio, sector_map, on='fundNo', how='left')
        else:
            raise ValueError('Invalid method')
        return portfolio_sector

    def get_sector_weighting(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        It could be directly based on the query you have above, but have one more step to do a groupby to generate the aggregate sum of weight for a cluster"""
        if method == 'SQL':
            self.generate_portfolio_tmp_table(portfolio)
            sector_weighting = self.conn.get_dataframe_from_sql_query("""
                SELECT c.main_cluster, c.sub_cluster, SUM(p.weight) AS weight
                FROM portfolio p LEFT JOIN clustering_output c ON p.fundNo=c.fundNo
                GROUP BY c.main_cluster, c.sub_cluster
                """)
        elif method == 'InMemory':
            portfolio_sector = self.portfolio_to_sector(portfolio, method='InMemory')
            sector_weighting = portfolio_sector.groupby(['main_cluster', 'sub_cluster']).sum()['weight']
            sector_weighting = sector_weighting.reset_index()
        else:
            raise ValueError('Invalid method')
        return sector_weighting

    def get_sector_map(self, method='SQL'):
        """
        You would expect to get a cluster mapping of each mutual fund from either some calculation based on your fund cluster strategy,
        a cached flat file, or database query, define this method accordingly based on the inheritance of your code

        Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL:For this one, it is just to load the mapping from sql"""

        sector_map = self.conn.get_dataframe('clustering_output', self.schema)

        return sector_map

    def load_underlying_ts(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: load the data from some other method or database that you already load
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        You would need to join table of ts of different fund, or
        filter ts base on fund ticker if you put all timeseries in one table"""
        if method == 'SQL':
            self.generate_portfolio_tmp_table(portfolio)
            underlying_ts_weight = self.conn.get_dataframe_from_sql_query("""
                SELECT p.fundNo AS p_fundNo, p.weight, m.*
                FROM portfolio p INNER JOIN morning_star m ON p.fundNo=m.fundNo
                """)
            underlying_ts_weight.drop('fundNo', axis=1, inplace=True)
            underlying_ts_weight.rename(columns={'p_fundNo': 'fundNo'}, inplace=True)
        elif method == 'InMemory':
            underlying_ts = self.conn.get_dataframe_from_sql_query("SELECT * FROM morning_star")
            underlying_ts_weight = pd.merge(portfolio, underlying_ts, on='fundNo', how='inner')
        else:
            raise ValueError('Invalid method')
        return underlying_ts_weight

    def generate_portfolio_ts(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: do the calculation through python, you may need to load the underlying ts by some method, like load_underlying_ts
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        you would need to do the query that you have in load_underlying_ts, and do one more step in the query to sum the value
        for all funds to generate the value for the portfolio."""
        if method == 'SQL':
            underlying_ts_weight = self.load_underlying_ts(portfolio, method='SQL')
        elif method == 'InMemory':
            underlying_ts_weight = self.load_underlying_ts(portfolio, method='InMemory')
        else:
            raise ValueError('Invalid method')

        columns = ["per_com", "per_pref", "per_conv", "per_corp", "per_muni", "per_govt", "per_oth",
                   "per_cash", "per_bond", "per_abs", "per_mbs", "per_eq_oth", "per_fi_oth"]
        portfolio_ts = pd.DataFrame(columns=columns)

        if len(underlying_ts_weight) > 0:
            grouped = underlying_ts_weight.groupby('date')
            for column in columns:
                portfolio_ts[column] = grouped.apply(lambda x: (x[column]*x['weight']).sum())

        return portfolio_ts
