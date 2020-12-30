

# Local Imports
import Config
import DataHelper
from .BaseDataCatcher import BaseDataCatcher


class BaseCSVDataCatcher(BaseDataCatcher):

    def __init__(self, **kwargs):

        self.reader = DataHelper.get_data_reader(source='csv')

        super().__init__(self.reader)


    def load_data(self, verbose=True, **kwargs):

        if verbose:
            print("Loading data...")

        for path_key, (db_name, table_name) in self.DATA_NEEDS.items():
            self.reader.load_table(db_name, table_name, Config.DATA_PATHS[path_key], **kwargs)

        if verbose:
            print("... Finished loading data")
