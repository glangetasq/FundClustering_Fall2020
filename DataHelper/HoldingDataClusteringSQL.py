
# redefine the data input function and output function in your derived FundClusterStrategy Class using SQL query to enable database connection
# to handle data processing, please follow the provide python package on how to update a table, you need to provide a table template as configuration
# of the table, and use the configuration to update the sql table, please setup your own sql db in your local machine and test based on it
# The following show some function that you need to define in your derived strategy class

from Models import HoldingDataMainClustering
import os
from sauma.core import Connection

os.environ['SECRETS_DIR'] = '/Users/glangetasq'

class HoldingDataClusteringSQL(HoldingDataMainClustering, SQLHandlerMixin):
    """Inlcude SQL Operation in Mutual Fund Performance Feature Calculation"""
    def setup_table_templates(self):
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
        as the sauma.core package require a json obj as input, you may need to transform the dictionary into a json obj by doing 
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

        TEMPLATE_TICKER = {
            "tableName": "ticker",
            "schema": "fund_clustering",
            "columns": [{"name": "fundNo", "type": "INTEGER"},
                        {"name": "fundTicker", "type": "STRING", "size": 10}],
            "primaryKey": ["fundNo"],
            "description": 'fund number and ticker'
        }

        TEMPLATE_RETURNS = {
            "tableName": "returns",
            "schema": "fund_clustering",
            "columns": [{"name": "fundNo", "type": "INTEGER"},
                        {"name": "date", "type": "DATE"},
                        {"name": "r", "type": "FLOAT", "size": 53}],
            "primaryKey": ["fundNo", "date"],
            "description": 'fund returns'
        }

        TEMPLATE_MORNINGSTAR = {
            "tableName": "morning_star",
            "schema": "fund_clustering",
            "columns": [{"name": "fundNo", "type": "INTEGER"},
                        {"name": "date", "type": "DATE"},
                        {"name": "per_com", "type": "FLOAT", "size": 53},
                        {"name": "per_pref", "type": "FLOAT", "size": 53},
                        {"name": "per_conv", "type": "FLOAT", "size": 53},
                        {"name": "per_corp", "type": "FLOAT", "size": 53},
                        {"name": "per_muni", "type": "FLOAT", "size": 53},
                        {"name": "per_govt", "type": "FLOAT", "size": 53},
                        {"name": "per_oth", "type": "FLOAT", "size": 53},
                        {"name": "per_cash", "type": "FLOAT", "size": 53},
                        {"name": "per_bond", "type": "FLOAT", "size": 53},
                        {"name": "per_abs", "type": "FLOAT", "size": 53},
                        {"name": "per_mbs", "type": "FLOAT", "size": 53},
                        {"name": "per_eq_oth", "type": "FLOAT", "size": 53},
                        {"name": "per_fi_oth", "type": "FLOAT", "size": 53},
                        {"name": "lipper_class_name", "type": "STRING", "size": 50}],
            "primaryKey": ["fundNo", "date"],
            "description": 'morningstar data for each fund'
        }

        self.template_ticker = TEMPLATE_TICKER
        self.template_returns = TEMPLATE_RETURNS
        self.template_morningstar = TEMPLATE_MORNINGSTAR
    
    def setup_tables(self):
        """setup all table based on the setup_table_Templates"""
        self.look_up_or_create_table(self.template_ticker)
        self.look_up_or_create_table(self.template_returns)
        self.look_up_or_create_table(self.template_morningstar)

    
    def __init__(self, username, password):
        super().__init__()
        self.setup_connection(username, password)
        self.setup_table_templates()
        self.setup_tables()


    def update_raw_data(self):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template"""
        pass
    