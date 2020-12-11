

class BaseDataReader:

    def __init__(self, reader_type=None):
        self.reader_type = reader_type
        self.dataframes = dict()


    def is_reader_type(self, reader_type):
        return self.reader_type == reader_type.lower()


    def _insert_new_dataframe(self, db_name, table_name, df):

        if not db_name in self.dataframes:
            self.dataframes[db_name] = dict()

        self.dataframes[db_name][table_name] = df


    def get_dataframe(self, db_name, table_name):

        if db_name in self.dataframes and table_name in self.dataframes[db_name]:
            return self.dataframes[db_name][table_name]
        else:
            raise ValueError(f"Tried to access {table_name} in the {db_name} database, before loading it.")


    def load_table(self):
        raise NotImplementedError("Children of BaseDataReader should have load_table implemented.")
