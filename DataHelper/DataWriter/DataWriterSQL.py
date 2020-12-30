
"""
Object that write a dataframe of fundNo, main_cluster, sub_cluster to a SQL table
"""

import os
import json
from sauma.core import Connection

# Local Imports
from .BaseDataWriter import BaseDataWriter
import Config
from DataHelper.SQLDataHandler import SQLDataHandler


class DataWriterSQL(BaseDataWriter, SQLDataHandler):
    """ Inlcude SQL Operation """

    def __init__(self, **kwargs):

        super().__init__()
        self.setup_connection(**kwargs)


    def setup_table_templates(self, template):
        """Define the all table template as local variable here, all these table template should be defined as a global variable in a
        python file, and import here for this class to use, please check the sauma.core documentation, the template format should be something like:
        """
        self.template = template


    def setup_tables(self, db_name, table_name):
        """ setup all table based on the setup_table_Templates """

        self.conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.conn.execute(f"USE {db_name}")

        self.drop_table(db_name, table_name)
        self.conn.create_table(json.dumps(self.template))


    def update_raw_data(self, dataframe, db_name=None, table_name=None, chunk_size=None):
        """assuming that your data source is the csv file containing all the raw data, load the raw data from csv, and update the table
        which you already setup based on your template

        Careful! It replaces all current data in the table to the dataframe data

        Input:
            - db_name: str, database name, or schema
            - table_name: str, table name
            - dataframe: pd.DataFrame, dataframe with correct column names, and type
        """

        template = Config.SQL.STRUCTURE.get(db_name, dict()).get(table_name, dict()).get('template')

        if template is None:
            raise ValueError(f"Could not find appropriate template for ({db_name}, {table_name})")

        self.setup_table_templates(template)
        self.setup_tables(db_name, table_name)

        if chunk_size:
            self.chunks_update_table(db_name, table_name, dataframe, chunk_size = 100000)
        else:
            self.conn.update_table(
                table_name = table_name,
                schema = db_name,
                dataframe = dataframe,
                index = False,
                if_exists = 'replace',
            )
