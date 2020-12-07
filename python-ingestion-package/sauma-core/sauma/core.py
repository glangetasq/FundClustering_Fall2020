""" Sauma Core """
import os
import json
import platform
import pprint
import pandas as pd
from sauma.config import WINDOWS, SECRETS_FILE, DB_META, PRIMARY_KEY
from sauma.config import HOST, TYPE_MAPPER, SAUMA_KEYWORDS
from getpass import getpass
from sqlalchemy import create_engine, inspect, Table
from sqlalchemy import MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import ResultProxy
from sqlalchemy.schema import Column


class Connection(object):
    """
    This class defines the various functionality of sauma core
    """

    def __init__(self, username: str = None, password: str = None, schema: str = None) -> 'sauma.core.Connection':

        """
        Initialize the connection to sauma core
        
        To read the credentials from a secrets file, set the environment variable SECRETS_DIR 
        pointing to the directory containing .saumapass file 

        if the environment variable is not set then a default home directory would be assumed

        for a MAC and LINUX system, the default directory is ~/ and for the Windows system
        C:\\Users\\$user 
        
        The format of .saumapass is $username:$password:$schema

        Keyword Args:
            username (str): the username of the user
            password (str): the password used for the sauma core system
            schema (str): the name of the schema to establish connection

        Returns:
            sauma.core.Connection object
        """

        # get the default path based on the underlying OS
        default_path = self.__get_default_path()

        path = os.getenv('SECRETS_DIR', default_path)

        # check if credentials are stored in the secrets file.
        # If so retrieve them
        credentials = self.__get_params_from_secrets(path)
        if credentials:
            self.username = credentials[0]
            self.password = credentials[1]
            if len(credentials) > 2:
                self.schema = credentials[2]
            else:
                self.schema = ''
        else:
            if username:
                self.username = username
            else:
                print("Enter username: ")
                self.username = input()
            if password:
                self.password = password
            else:
                print('Enter password: ')
                self.password = getpass()
            if schema or schema == '':
                self.schema = schema
            else:
                print('Enter schema(optional): ')
                self.schema = input()

        # set the pretty printer with indent = 4
        self.pp = pprint.PrettyPrinter(indent=4)

        # check if connect has been executed
        self.__connect = False

        # initialize engine to None
        self.engine = None

        # initialize inspector to None
        self.inspector = None

    def connect(self, schema: str = None) -> 'sqlalchemy.engine.Connection':
        """
        This methods connects with the sauma core.
        Args:
            schema: defaults to the schema provided during initialization

        Returns:
            sqlalchemy.engine.Connection
        """

        # set the default schema
        if not schema:
            schema = self.schema
        path = self.__generate_conn_path(schema)
        self.engine = create_engine(path)

        # initialize inspector attribute
        # would be useful with show schemas and show tables
        self.inspector = inspect(self.engine)

        # mark the connection as true
        self.__connect = True
        return self.engine.connect()

    def show_schemas(self) -> None:
        """
        This method prints all the schemas defined in the system as a list
        Needs the connection to be initialized before
        """
        if not self.__connect:
            raise ProgrammingError('No connection established! You can establish the connection by calling' + \
                                   ' self.connect()', None, None)
        db_list = self.inspector.get_schema_names()
        self.pp.pprint(db_list)

    def show_tables(self, schema: str) -> None:
        """
        prints out the names of tables in a given schema
        """
        if not self.__connect:
            raise ProgrammingError('No connection established! You can establish the connection by calling' + \
                                   ' self.connect()', None, None)
        tables = self.inspector.get_table_names(schema=schema)
        self.pp.pprint(tables)

    def get_table(self, table_name: str, schema: str) -> Table:
        """
        This method queries the database for the table

        Args:
            table_name: The name of the table
            schema: Name of the schema
        Returns:
            sqlalchemy.Table
        """

        # create the engine
        uri = self.__generate_conn_path(schema)
        engine = create_engine(uri)

        # get metadata
        metadata = MetaData(engine)
        metadata.reflect(bind=engine)

        if not metadata:
            raise (ProgrammingError(f"{table_name} does not exist in {schema}", table_name, schema))

        # get all tables in the metadata
        tables = metadata.tables

        # dispose off all the connections by engine
        engine.dispose()

        # check and return if the table exist otherwise raise ProgrammingError
        if table_name in tables:
            return tables[table_name]

        raise (ProgrammingError(f"{table_name} does not exist in {schema}", table_name, schema))

    def execute(self, query: str) -> ResultProxy:
        """
        This method executes a raw sql query and returns a ResultProxy
        For more information check 
        https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.ResultProxy

        Args:
            query: SQL query to execute
        Returns:
            sqlalchemy.engine.ResultProxy
        """
        return self.engine.execute(query)

    def create_table(self, definition: 'JSON'):
        """
        Input should be a well formatted JSON object as per below:

        1. `table_name`is mandatory keys for the json object
        2. `schema` name of the schema
        3. All other columns are considered to be columns in the table and their type 
        should follow the structure of SQLAlchemy. For further information on typing 
        https://docs.sqlalchemy.org/en/13/core/type_basics.html
        Also for quick reference check 
        https://stackoverflow.com/questions/30137806/where-can-i-find-a-list-of-the-flask-sqlalchemy-column-types-and-options
        4. The column description should be added as a dictinary. `type` key as shown in the example below is mandatory, all others
        should be the keywor arguments as used in sqlalchemy types  
        5. `primary_key` can be a key for a column with a boolean value True

        A sample JSON
        {
            "table_name": "Test",
            "schema": "test_db",
            "id": {
                    "type":"INTEGER", // case insensitive
                    "primary_key": True
                    },
            "text_col": {
                        "type":"STRING",
                        "length":50
                        },
            "int_col": {
                    "type":"INT"
                    } 
        }

        Args:
            definition: A json object

        Returns:
            None

        Raises:
            InternalError
                If table already exists
        """
        definition_dict = json.loads(definition)
        schema = definition_dict['schema']
        table_name = definition_dict['table_name']

        # drop sauma keywords from defintion_dict
        definition_dict = self.__remove_keys_from_dict(definition_dict, SAUMA_KEYWORDS)

        # Create a list of sqlalchemy columns
        columns = []
        for key in definition_dict.keys():

            # column keyword arguments
            col_kwargs = definition_dict[key]

            # column type String, Int, etc
            col = col_kwargs['type']
            primary_key = col_kwargs.get(PRIMARY_KEY, False)

            # column description keyword arguments as dict
            col_kwargs.pop('type')

            if PRIMARY_KEY in col_kwargs:
                col_kwargs.pop(PRIMARY_KEY)

            # append sqlalchemy columns
            columns.append(Column(key, TYPE_MAPPER[col.lower()](**col_kwargs), primary_key=primary_key))

        # create engine for table
        dburi = self.__generate_conn_path(schema)
        engine = create_engine(dburi)

        # metadata
        meta = MetaData(engine)

        table = Table(table_name, meta, *columns)
        table.create()

        # dispose off all the connections in the engine
        engine.dispose()

    def update_table(self, table_name: str, dataframe: pd.DataFrame,
                     schema: str = None, **kwargs):
        """
        This method updates an existing table based on an action
        For reference https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

        Args:
            table_name: Name of the table to update
            dataframe: A pandas dataframe 
            schema: defaults to current schema

        Kwargs:
            **if_exists**: {‘fail’, ‘replace’, ‘append’}, default ‘fail’
                How to behave if the table already exists.
                    fail: Raise a ValueError.
                    replace: Drop the table before inserting new values.
                    append: Insert new values to the existing table.

            **index**: bool, default True
                Write DataFrame index as a column. Uses index_label as the column name in the table.

            **index_label**: str or sequence, default None
                Column label for index column(s). If None is given (default) and index is True, then the index names
                are used.A sequence should be given if the DataFrame uses MultiIndex.

            **chunksize**: int, optional
                Specify the number of rows in each batch to be written at a time. By default, all rows will be written
                 at once.

            **dtype**: dict or scalar, optional
                Specifying the datatype for columns. If a dictionary is used, the keys should be the column names and
                the values should be the SQLAlchemy types or strings for the sqlite3 legacy mode. If a scalar is
                provided, it will be applied to all columns.

            **method**: {None, ‘multi’, callable}, optional
                Controls the SQL insertion clause used:
                    None : Uses standard SQL INSERT clause (one per row).
                    ‘multi’: Pass multiple values in a single INSERT clause.
                    callable with signature (pd_table, conn, keys, data_iter).
                    Details and a sample callable implementation can be found in the section insert method of
                    pandas documentation.

        Returns:
            None

        Raises:
            ValueError
                if if_exists is 'fail' which is default
        """
        dataframe.to_sql(table_name, self.engine, schema=schema, **kwargs)

    def get_dataframe(self, table_name: str, schema: str, **kwargs) -> pd.DataFrame:
        """
        For ref:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_table.html#pandas.read_sql_table
        Args:
            table_name: Name of the table
            schema: Name of the schema
        Kwargs:
            index_col: str or list of str, optional, default: None
                Column(s) to set as index(MultiIndex).

            coerce_float: bool, default True
                Attempts to convert values of non-string, non-numeric objects (like decimal.Decimal) to floating point.
                 Can result in loss of Precision.

            parse_dates: list or dict, default None
                List of column names to parse as dates.

                Dict of {column_name: format string} where format string is strftime compatible in case of parsing
                 string times or is one of (D, s, ns, ms, us) in case of parsing integer timestamps.

                Dict of {column_name: arg dict}, where the arg dict corresponds to the keyword arguments of
                 pandas.to_datetime() Especially useful with databases without native Datetime support, such as SQLite.

            columns: list, default None
                List of column names to select from SQL table.

            chunksize: int, default None
                If specified, returns an iterator where chunksize is the number of rows to include in each chunk.
        Returns:
            pd.DataFrame
                A SQL table is returned as two-dimensional data structure with labeled axes.
        """
        return pd.read_sql_table(table_name, self.engine, schema, **kwargs)

    def get_dataframe_from_sql_query(self, sql, **kwargs):
        """
        Ref:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_query.html#pandas.read_sql_query
        Args:
            sql: SQL Query
        Kwargs:
            index_col: str or list of strings, optional, default: None
                Column(s) to set as index(MultiIndex).

            coerce_float: bool, default True
                Attempts to convert values of non-string, non-numeric objects (like decimal.Decimal) to floating point.
                 Useful for SQL result sets.

            parse_dates: list or dict, default: None
                List of column names to parse as dates.

                Dict of {column_name: format string} where format string is strftime compatible in case of parsing
                 string times, or is one of (D, s, ns, ms, us) in case of parsing integer timestamps.

                Dict of {column_name: arg dict}, where the arg dict corresponds to the keyword arguments of
                pandas.to_datetime() Especially useful with databases without native Datetime support, such as SQLite.

                chunksize: int, default None
                    If specified, return an iterator where chunksize is the number of rows to include in each chunk.
        Returns:
            DataFrame
        """
        return pd.read_sql_query(sql, self.engine, **kwargs)

    def close(self):
        """
        This method closes the connection to sauma core
        will close all the connections of the connection pool
        """
        self.engine.dispose()

    def __get_default_path(self):
        system = platform.system()
        user = os.getlogin()
        if system == WINDOWS:
            default_path = f"C:\\Users\\{user}"
        else:
            default_path = f"/home/{user}"
        return default_path

    def __get_params_from_secrets(self, path):

        # check if the path contains .saumapass file
        if SECRETS_FILE in os.listdir(path):
            file_path = os.path.join(path, SECRETS_FILE)
            with open(file_path, 'r') as f:
                return tuple(f.read().strip().split(':'))
        return

    def __generate_conn_path(self, schema=None):
        if not schema:
            schema = ''
        else:
            schema = f'/{schema}'
        return f'{DB_META}://{self.username}:{self.password}@{HOST}{schema}'

    def __remove_keys_from_dict(self, dict_, keys):
        [dict_.pop(key, None) for key in keys]
        return dict_

    def __get_engine(self, schema):
        if schema:
            dburi = self.__generate_conn_path(schema)
            engine = create_engine(dburi)
        else:
            engine = self.engine
        return engine
