
import pandas as pd
from sauma.core import Connection
from sqlalchemy import select


# Local imports
from config import SQL_CONFIG
from .BaseDataReader import BaseDataReader

class DataReaderSQL(BaseDataReader):

    def __init__(self, username, password, schema):

        super().__init__(reader_type='sql')
        self.c = None


    def setup_connection(self, username=None, password=None, schema=None, secrets_dir=None):
        """initilize the connection obj here, and use it for any operation

        Optional Inputs :
            - username : str, use default username if None
            - password : str, use default password if None
            - schema : str, use default schema if None
            - screts_dir : str, use default secrets_dir if None
        """

        default_login = SQL_CONFIG['default_login']
        username = username if username is not None else default_login['username']
        password = password if password is not None else default_login['password']
        schema = schema if schema is not None else default_login['schema']
        secrets_dir = secrets_dir if secrets_dir is not None else default_login['secrets_dir']

        os.environ['SECRETS_DIR'] = secrets_dir
        self.c = Connection(username = username, password = password, schema = '')
        self.c.connect()


    def _check_if_connected(self):

        if not self.c:
            raise Error("setup_connection of DataReaderSQL before trying to read data.")


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


        db_name = SQL_CONFIG['database']
        table_name = SQL_CONFIG['tables']['returns']
        table = self.c.get_table(table_name, db_name)

        # Use database
        self.c.execute(f"USE {db_name}")

        # SQL that takes into account if at least one of t_lower/t_upper is None
        sql = select([table])
        if t_lower:
            sql = sql.where(table.c.date >= t_lower)
        if t_upper:
            sql = sql.where(table.c.date <= t_upper)

        # Get the returns we are interested in
        returns = self.c.get_dataframe_from_sql_query(sql, parse_dates=['date'])

        # From flat dataframe to matrix like dataframe
        returns = returns.pivot(index='date', columns='fundNo', values='r')
        # returns.index = pd.to_datetime(returns.index)

        return returns


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

        db_name = SQL_CONFIG['database']
        table_name = SQL_CONFIG['tables']['holding_asset']
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

        db_name = SQL_CONFIG['database']
        table_name = SQL_CONFIG['tables']['morningstar']
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

        db_name = SQL_CONFIG['database']
        table_name = SQL_CONFIG['tables']['morningstar']
        fundno_ticker = self.c.get_dataframe(table_name, db_name)

        # Convert to dict
        fundno_ticker = pd.Series(fundno_ticker['ticker'].values, index=df['fundNo']).to_dict()

        return fundno_ticker
