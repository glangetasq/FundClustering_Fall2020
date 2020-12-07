
# please define the setup_connection in this class

from BaseClasses import SQLHandlerMixin
import os
import json
from sauma.core import Connection
from Config import SQL

DEFAULT_USERNAME = SQL.login.default_username
DEFAULT_PASSWORD = SQL.login.default_password
DEFAULT_SECRETS_DIR = SQL.login.default_secrets_dir

class SQLDataHandler(SQLHandlerMixin):
    """Mixin class that you would include in the inheritance hierarchy to migarte all possible operation to SQL
    so as to speed up calculation, you would need to integrate the sauma.core package and utilize the connection obj here"""

    def __init__(self):
        super().__init__()

    def setup_connection(self, secrets_dir = None, username = None, password = None):
        """initilize the connection obj here, and use it for any operation"""

        secrets_dir = secrets_dir if secrets_dir is not None else DEFAULT_SECRETS_DIR
        username = username if username is not None else DEFAULT_USERNAME
        password = password if password is not None else DEFAULT_PASSWORD

        os.environ['SECRETS_DIR'] = secrets_dir
        self.conn = Connection(username = username, password = password, schema = '')
        self.conn.connect()


    def setup_table_template(self):
        """define the table template as local variable in this method for all derived class, and utilize this method to setup tables"""
        raise NotImplementedError("Derived Class need to implement this method")


    def check_table_exist_or_not(self, schemas, table_name):
        """Please define this method to check whether a table under certain schemas exist or not"""

        self.conn.execute("USE " + schemas + ";")
        sql = "IF (EXISTS (SELECT * FROM " + schemas + "." + table_name + " )) " + \
                 "BEGIN PRINT 'Table Exists' RETURN 1; END"
        return self.conn.execute(sql)


    def look_up_or_create_table(self, template, custom_table_name=None, custom_schemas_name=None):
        """Please define this method to create a table based on the template if a table does not exist, do nothing if table already exist,
        you may want to use self.check_table_exist_or_not here, if custom_table_name is none, you should be able to find it in template"""

        if self.check_table_exist_or_not(custom_schemas_name, custom_table_name) == 1:
            print('Table already exists\n')
        else:
            self.conn.execute("CREATE DATABASE IF NOT EXISTS " + custom_schemas_name + ";")
            self.conn.execute("USE "+ custom_schemas_name + ";")

            template["schema"] = custom_schemas_name
            template["table_name"] = custom_table_name
            self.conn.create_table(json.dumps(template))
            print('Table created successfully\n')


    def drop_table(self, schemas, table_name):

        self.conn.execute('USE ' + schemas + ';')
        sql = "DROP TABLE IF EXISTS " + schemas + "." + table_name + ";"
        self.conn.execute(sql)


    def chunks_update_table(self, schema, table_name, dataframe, **kwargs):
        """when you have a large dataframe, it mays takes a long time to update the sql table if you upload it at once, you could actually
        divide the table into smaller chunks and upload them piece by piece to speed up the process, as it is more memory efficient and use less cpu,
        try to implement this method here too"""

        chunk_size = kwargs.get('chunk_size', None)
        if_exists = kwargs.get('if_exists', 'append')
        N = dataframe.shape[0]

        self.conn.execute('USE ' + schema + ';')

        for i in range(N // chunk_size + 1):
            print(f"Inserting chunk {i+1}/{N//chunk_size + 1}")
            df_to_insert = dataframe.iloc[i*N:(i+1)*N]
            self.conn.update_table(table_name = table_name,
                    schema = schema,
                    dataframe = df_to_insert,
                    index = False,
                    if_exists = if_exists
                    )
