
# redefine the data input function and output function in your derived FundClusterStrategy Class using SQL query to enable database connection
# to handle data processing, please follow the provide python package on how to update a table, you need to provide a table template as configuration
# of the table, and use the configuration to update the sql table, please setup your own sql db in your local machine and test based on it
# The following show some function that you need to define in your derived strategy class

import os
import numpy as np
import pandas as pd
import json
from sauma.core import Connection

# Local Imports
from config import PATHS
from DataHelper.CSVtoSQL.SQLDataHandler import SQLDataHandler
from Models import HoldingDataMainClustering

# Get paths
TICKER_PATH = PATHS['ticker']
RETURNS_PATH = PATHS['returns']
MORNING_STAR_PATH = PATHS['morningstar']


class HoldingDataMainClusteringSQL(HoldingDataMainClustering, SQLDataHandler):
    """ Inlcude SQL Operation in first layer fund clustering """

    def setup_table_templates(self):
        """Define the all table template as local variable here, all these table template should be defined as a global variable in a
        python file, and import here for this class to use, please check the sauma.core documentation
        """

        TEMPLATE_RESULTS = {
            "tableName": "firstlayer_cluster_results",
            "schema": "fund_clustering",
            "columns": [{"name": "Fund.No", "type": "INTEGER"},
                        {"name": "Ticker", "type": "STRING", "size": 10},
                        {"name": "Cluster", "type": "INTEGER"},
                        {"name": "Cash", "type": "FLOAT"},
                        {"name": "Equity", "type": "FLOAT"},
                        {"name": "Bond", "type": "FLOAT"},
                        {"name": "Security", "type": "FLOAT"},
                        {"name": "Mstar Category", "type": "STRING", "size": 53},
                        {"name": "Cluster Category", "type": "STRING", "size": 50},
                        {"name": "sharpe_ratio", "type": "STRING", "size": 50},
                        {"name": "absolute_return", "type": "STRING", "size": 10},
                        {"name": "absolute_return_val", "type": "FLOAT"}],                      
            "primaryKey": ["Fund.No"],
            "description": 'Main cluster results'
        }

        self.template_results= TEMPLATE_RESULTS
 

    def setup_tables(self, schema):
        """ setup all table based on the setup_table_Templates """

        self.schema = schema
        self.conn.execute("CREATE DATABASE IF NOT EXISTS " + schema + ";")
        self.conn.execute('USE ' + schema + ';')

        self.drop_table(self, schema, "firstlayer_cluster_results")
        self.conn.create_table(json.dumps(self.template_results))


    def __init__(self, secrets_dir, username, password):
        super().__init__()

        self.setup_connection(secrets_dir, username, password)
        self.setup_table_templates()
        self.setup_tables()


    def update_raw_data(self):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template"""

        pass
