# Data Helper

from .DataCache import DataCache
from .DataPreProcessor import DataPreProcessor
from .DataProcessor import DataProcessor
from .DataReader import DataReader


def get_data_reader():
    return DataReader()

@staticmethod
def get_data_preprocessor():
    return DataPreProcessor()

@staticmethod
def get_data_cache(clustering_year):
    reader = DataHelper.get_data_reader()
    preprocessor = DataHelper.get_data_preprocessor()
    return DataCache(reader, preprocessor, clustering_year)

@staticmethod
def get_data_processor():
    return DataProcessor()
