
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


    def _insert_new_dataframe(self, db_name, table_name, df):

        if not db_name in self.dataframes:
            self.dataframes[db_name] = dict()

        self.dataframes[db_name][table_name] = df


    def load_table(self, db_name, table_name, parse_dates=[]):

        # Load only once
        if not(db_name in self.dataframes and table_name in self.dataframes[db_name]):

            self._check_if_connected()

            request = Config.SQL.STRUCTURE[db_name][table_name]['request']
            parse_dates = Config.SQL.STRUCTURE[db_name][table_name].get('parse_dates', [])

            self.c.execute(f"USE {db_name}")
            df = self.c.get_dataframe_from_sql_query(request, parse_dates=parse_dates)

            self._insert_new_dataframe(db_name, table_name, df)


    def get_dataframe(self, db_name, table_name):

        if db_name in self.dataframes and table_name in self.dataframes[db_name]:
            return self.dataframes[db_name][table_name]
        else:
            raise ValueError(f"Tried to access {table_name} in the {db_name} database, before loading it.")


    def get_returns(self, t_lower=None, t_upper=None):
        """
        Get the returns from the database that satisfies t_lower <= t <= t_upper

        Input:
            - t_lower : string in 'YYYY-MM-DD' format
            - t_upper : string in 'YYYY-MM-DD' format
        Output:
            - returns : pd.DataFrame with time index and fund number columns
        """

        self._check_if_connected()


        db_name = Config.SQL.login.default_db
        table_name = 'returns'
        table = self.c.get_table(table_name, db_name)

        # Use database
        self.c.execute(f"USE {db_name}")

        # SQL that takes into account if at least one of t_lower/t_upper is None
        sql = select([table])
        if t_lower:
            sql = sql.where(table.c.date >= t_lower)
        if t_upper:
            sql = sql.where(table.c.date <= t_upper)

        print(sql)

        return None


    def get_holding_asset(self, year, month=12, day=None):
        """
        Get the holding_asset data from the database for a specific date

        Input:
            - year : int
            - month : int
            - day : int or None (not used if None)
        Output:
            - holding_asset : pd.DataFrame
        """

        self._check_if_connected()

        db_name = SQL.login.default_db
        table_name = SQL.STRUCTURE[db_name]['holding_asset']
        table = self.c.get_table(table_name, db_name)

        # Use database
        self.c.execute(f"USE {db_name}")

        # Select the relevant columns and preprocess them if necessary
        sql = f"""
            SELECT
                fundNo,
                date,
                per_cash as cash,
                per_com + per_pref + per_eq_oth as equity,
                per_conv + per_corp + per_muni + per_govt as bond,
                per_abs + per_mbs + per_fi_oth + per_oth as sec
            FROM {table_name}
            WHERE
                YEAR(date) = {year}
            AND MONTH(date) = {month}
        """

        if day is not None:
            sql += f"AND DAY(date) = {day}"

        # Get the holding_asset data we are interested in
        holding_asset = self.c.get_dataframe_from_sql_query(sql, parse_dates=['date'])

        return holding_asset


    def get_fund_mrnstar(self, year, month=12, day=None):
        """
        Get the fund_morningstar data from the database for a specific date

        Input:
            - year : int
            - month : int
            - day : int or None (not used if None)
        Output:
            - fund_morningstar : pd.DataFrame
        """

        self._check_if_connected()

        db_name = SQL.login.default_db
        table_name = SQL.STRUCTURE[db_name]['morningstar']
        table = self.c.get_table(table_name, db_name)

        # Use database
        self.c.execute(f"USE {db_name}")

        # Select the relevant columns and preprocess them if necessary
        sql = f"""
            SELECT
                fundNo,
                date,
                lipper_class_name
            FROM {table_name}
            WHERE
                YEAR(date) = {year}
            AND MONTH(date) = {month}
        """

        if day is not None:
            sql += f"AND DAY(date) = {day}"

        # Get the holding_asset data we are interested in
        fund_morningstar = self.c.get_dataframe_from_sql_query(sql)

        return fund_morningstar


    def get_fundno_ticker(self):
        """
        Get the dictionary from fund number to ticker

        Output:
            - fundno_ticker : dict (key:fundNo, value:ticker)
        """

        self._check_if_connected()

        db_name = SQL.login.default_db
        table_name = SQL.STRUCTURE[db_name]['morningstar']
        fundno_ticker = self.c.get_dataframe(table_name, db_name)

        # Convert to dict
        fundno_ticker = pd.Series(fundno_ticker['ticker'].values, index=fundno_ticker['fundNo']).to_dict()

        return fundno_ticker
