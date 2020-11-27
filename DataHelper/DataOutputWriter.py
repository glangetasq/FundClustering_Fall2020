
"""
Object that write a dataframe of fundNo, main_cluster, sub_cluster to a SQL table
"""

import os
import json
from sauma.core import Connection

# Local Imports
from .SQLDataHandler import SQLDataHandler


class DataOutputWriter(SQLDataHandler):
    """ Inlcude SQL Operation in first layer fund clustering """

    def __init__(self, secrets_dir=None, username=None, password=None):

        super().__init__()
        self.setup_connection(secrets_dir, username, password)
        self.setup_table_templates()
        self.setup_tables()


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

        self.table_name = "clustering_output"

        TEMPLATE_OUTPUT = {
            "tableName": f"{self.table_name}",
            "schema": "fund_clustering",
            "columns": [{"name": "fundNo", "type": "INTEGER"},
                        {"name": "main_cluster", "type": "INTEGER"},
                        {"name": "sub_cluster", "type": "INTEGER"}],
            "primaryKey": ["fundNo"],
            "description": 'fund number and cluster result'
        }

        self.template_output = TEMPLATE_OUTPUT



    def setup_tables(self, schema='fund_clustering'):
        """ setup all table based on the setup_table_Templates """

        self.schema = schema
        self.conn.execute("CREATE DATABASE IF NOT EXISTS " + schema + ";")
        self.conn.execute('USE ' + schema + ';')

        self.drop_table(schema, "clustering_output")
        self.conn.create_table(json.dumps(self.template_output))


    def update_raw_data(self, output_frame):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template"""

        output_frame.columns = ['fundNo', 'main_cluster', 'sub_cluster']

        self.conn.update_table(
            table_name = self.table_name,
            schema = self.schema,
            dataframe = output_frame,
            index = False,
            if_exists = 'replace'
        )
