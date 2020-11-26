
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
from .SQLDataHandler import SQLDataHandler
from .morning_star_formatting_config import mrnstar_formatting_dict, mrnstar_new_name_dict

# Get paths
TICKER_PATH = PATHS['ticker']
RETURNS_PATH = PATHS['returns']
MORNING_STAR_PATH = PATHS['morningstar']


class MakeDatabaseSQL(SQLDataHandler):
    """ Inlcude SQL Operation in first layer fund clustering """

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

    def setup_tables(self, schema):
        """ setup all table based on the setup_table_Templates """

        self.schema = schema
        self.conn.execute("CREATE DATABASE IF NOT EXISTS " + schema + ";")
        self.conn.execute('USE ' + schema + ';')

        self.drop_table(self, schema, "ticker")
        self.drop_table(self, schema, "returns")
        self.drop_table(self, schema, "morning_star")
        self.conn.create_table(json.dumps(self.template_ticker))
        self.conn.create_table(json.dumps(self.template_returns))
        self.conn.create_table(json.dumps(self.template_morningstar))


    def __init__(self, secrets_dir, username, password):
        super().__init__()

        self.setup_connection(secrets_dir, username, password)
        self.setup_table_templates()
        self.setup_tables()


    def update_raw_data(self):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template"""

        # update ticker
        ticker = pd.read_csv(TICKER_PATH)
        columns = ['crsp_fundno', 'ticker']
        ticker = ticker[columns]
        ticker.columns = ['fundNo', 'fundTicker']
        ticker = ticker.drop_duplicates(subset=['fundNo'])
        self.chunks_update_table(self, self.schema, 'ticker', ticker, chunk_size = 100000)

        # update returns
        returns = pd.read_csv(RETURNS_PATH, parse_dates=True)
        returns = pd.wide_to_long(returns, '', i='date', j='fundNo')
        returns.columns = ['r']
        self.chunks_update_table(self, self.schema, 'returns', returns, chunk_size = 100000)

        # update morningstar
        mrnstar = pd.read_csv(MORNING_STAR_PATH)
        for colname in mrnstar:

            formatting_function = mrnstar_formatting_dict.get(colname, None)

            if formatting_function:
                mrnstar[colname] = formatting_function(mrnstar[colname])
            else:
                mrnstar = mrnstar.drop(colname, axis=1)

        mrnstar = mrnstar.rename(columns=mrnstar_new_name_dict)
        self.chunks_update_table(self, self.schema, 'morning_star', mrnstar, chunk_size = 10000)
