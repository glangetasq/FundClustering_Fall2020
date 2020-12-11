
import pandas as pd

# Local imports
from Config import DATA_PATHS
from .BaseDataReader import BaseDataReader


class DataReaderCSV(BaseDataReader):
    """
    Nothing fancy, just to stay coherent with the SQL implementation.
    """

    def __init__(self):
        super().__init__(reader_type='csv')


    def load_table(self, db_name, table_name, path, **kwargs):

        df = pd.read_csv(path, **kwargs)
        self._insert_new_dataframe(db_name, table_name, df)
