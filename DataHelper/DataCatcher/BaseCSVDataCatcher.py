

# Local Imports
import Config
from DataHelper import DataHelper
from .BaseDataCatcher import BaseDataCatcher


class BaseCSVDataCatcher(BaseDataCatcher):

    def __init__(self, **kwargs):

        csv_reader = DataHelper.get_data_reader(source='csv')

        super().__init__(csv_reader)


    def load_data(self, verbose=True):

        if verbose:
            print("Loading data...")

        for path_key, (db_name, table_name) in self.DATA_NEEDS.items():
            self.reader.load_table(db_name, table_name, Config.DATA_PATHS[path_key])

        if verbose:
            print("... Finished loading data")
