
import os
import pandas as pd
from sauma.core import Connection
from sqlalchemy import select


# Local imports
import Config
from .BaseDataReader import BaseDataReader

class DataReaderSQL(BaseDataReader):
    """
    Read and save any table from SQL using the requests in the Config

    It uses a Singleton Design Pattern: only one instance (at most)
        can exist in the system.
    Potential Problem: if we need several DataReaderSQL for different TMIN, TMAX
        this class will need to be adjusted.
    """

    __instance = None


    def __init__(self):
        raise RuntimeError('Call instance() instead')


    @classmethod
    def instance(cls, **kwargs):

        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            super(cls, cls.__instance).__init__(reader_type='sql')
            cls.__instance.c = None
            cls.__instance.setup_connection(**kwargs)

        return cls.__instance


    def setup_connection(self, **kwargs):
        """initilize the connection obj here, and use it for any operation

        Optional Inputs :
            - username : str, use default username if not defined
            - password : str, use default password if not defined
            - schema : str, use default schema if not defined
            - screts_dir : str, use default secrets_dir if not defined
        """

        username = kwargs.get('username', Config.SQL.login.default_username)
        password = kwargs.get('password', Config.SQL.login.default_password)
        schema = kwargs.get('schema', Config.SQL.login.default_schema)
        secrets_dir = kwargs.get('secrets_dir', Config.SQL.login.default_secrets_dir)

        os.environ['SECRETS_DIR'] = secrets_dir
        self.c = Connection(username = username, password = password, schema = '')
        self.c.connect()


    def _check_if_connected(self):

        if not self.c:
            raise ConnectionError("setup_connection of DataReaderSQL before trying to read data.")


    def load_table(self, db_name, table_name, parse_dates=[]):

        # Load only once
        if not(db_name in self.dataframes and table_name in self.dataframes[db_name]):

            self._check_if_connected()

            request = Config.SQL.STRUCTURE[db_name][table_name]['request']
            parse_dates = Config.SQL.STRUCTURE[db_name][table_name].get('parse_dates', [])

            self.c.execute(f"USE {db_name}")
            df = self.c.get_dataframe_from_sql_query(request, parse_dates=parse_dates)

            self._insert_new_dataframe(db_name, table_name, df)
