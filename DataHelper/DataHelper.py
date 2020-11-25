# Data Helper

from .DataCache import DataCache
from .DataMaker import DataMaker
from .DataPreProcessor import DataPreProcessor
from .DataProcessor import DataProcessor
from .DataReader import *


def get_data_reader(source='sql', username=None, password=None, schema=None):

    if source.lower() == 'csv':

        return DataReaderCSV()

    elif source.lower() == 'sql':

        return DataReaderSQL(username=username, password=password, schema=schema)



def get_data_preprocessor():
    return DataPreProcessor()


def get_data_cache(clustering_year):
    reader = get_data_reader()
    preprocessor = get_data_preprocessor()
    return DataCache(reader, preprocessor, clustering_year)


def get_data_processor():
    return DataProcessor()


def get_data_maker(data_name=''):
    return DataMaker(data_name)
