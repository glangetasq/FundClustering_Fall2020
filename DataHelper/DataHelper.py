# Data Helper

from .DataMaker import DataMaker
from .DataWriter import DataWriter
from .DataReader import *
from .DataOutputWriter import DataOutputWriter


def get_data_reader(source='sql', username=None, password=None, schema=None):

    if source.lower() == 'csv':

        return DataReaderCSV()

    elif source.lower() == 'sql':

        return DataReaderSQL(username=username, password=password, schema=schema)



def get_data_preprocessor():

    return DataPreProcessor()


def get_data_cache(source, clustering_year, username=None, password=None, schema=None):

    if source.lower() == 'csv':

        reader = get_data_reader(source='csv')
        preprocessor = get_data_preprocessor()

    elif source.lower() == 'sql':

        reader = get_data_reader(source='sql', username=username, password=password, schema=schema)
        preprocessor = get_data_preprocessor()

    return DataCache(reader, preprocessor, clustering_year)


def get_data_processor():
    return DataProcessor()


def get_data_writer(**kwargs):
    return DataWriter(**kwargs)


def get_data_maker(data_name=''):
    return DataMaker(data_name)


def get_data_output_writer(secrets_dir=None, username=None, password=None):
    return DataOutputWriter(secrets_dir, username, password)
