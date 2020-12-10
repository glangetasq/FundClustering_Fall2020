

# Local Imports
from DataHelper import DataHelper
from .BaseDataCatcher import BaseDataCatcher


class BaseSQLDataCatcher(BaseDataCatcher):

    def __init__(self, **kwargs):

        sql_reader = DataHelper.get_data_reader(source='sql')
        sql_reader.setup_connection(**kwargs)

        super().__init__(sql_reader)


    def load_data(self, verbose=True):

        if verbose:
            print("Loading data...")

        for db_name, table_name in self.DATA_NEEDS:
            self.reader.load_table(db_name, table_name)

        if verbose:
            print("... Finished loading data")
