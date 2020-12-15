
import pandas as pd

# Local imports
from Config import DATA_PATHS
from .BaseDataReader import BaseDataReader


class DataReaderCSV(BaseDataReader):
    """
    Nothing fancy, just to stay coherent with the SQL implementation.
    """

    __instance = None


    def __init__(self):
        raise RuntimeError('Call instance() instead')


    @classmethod
    def instance(cls, **kwargs):

        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            super(cls, cls.__instance).__init__(reader_type='csv')

        return cls.__instance


    def load_table(self, db_name, table_name, path, **kwargs):

        df = pd.read_csv(path, **kwargs)
        self._insert_new_dataframe(db_name, table_name, df)
