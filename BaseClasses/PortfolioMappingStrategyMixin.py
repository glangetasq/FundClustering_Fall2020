class PortfolioMappingStrategyMixin:
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
        # add the new table template that you need here
        pass

    def setup_portfolio_tables(self):
        """setup all table based on the setup_table_Templates"""
        # add the new table setup here
        pass

    def generate_portfolio_tmp_table(self, portfolio):
        """generate a temp table that save the portfolio information"""
        pass

    def portfolio_to_sector(self, portfolio, method='SQL'):
        """
        Given a portfolio of mutual fund, with fund name/fund id and weight on each mutual fund, map the portfolio
        to the fund cluster definition, and generate a new data framework which provide information of the mapping

        Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        and join it with a table with the cluster mapping to get the mapping"""
        pass

    def get_sector_weighting(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        It could be directly based on the query you have above, but have one more step to do a groupby to generate the aggregate sum of weight for a cluster"""
        pass

    def get_sector_map(self, method='SQL'):
        """
        You would expect to get a cluster mapping of each mutual fund from either some calculation based on your fund cluster strategy,
        a cached flat file, or database query, define this method accordingly based on the inheritance of your code

        Method could accept two kind of arguments:
        InMemory: do the calculation through python
        SQL:For this one, it is just to load the mapping from sql"""
        raise ValueError('Need to implement get_sector_mapping in derived class')

    def load_underlying_ts(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: load the data from some other method or database that you already load
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        You would need to join table of ts of different fund, or
        filter ts base on fund ticker if you put all timeseries in one table"""
        pass

    def generate_portfolio_ts(self, portfolio, method='SQL'):
        """Method could accept two kind of arguments:
        InMemory: do the calculation through python, you may need to load the underlying ts by some method, like load_underlying_ts
        SQL: So for this case, you would want to create a temperate table in SQL to strore portfolio info by running generate_portfolio_tmp_table,
        you would need to do the query that you have in load_underlying_ts, and do one more step in the query to sum the value
        for all funds to generate the value for the portfolio."""
        pass
