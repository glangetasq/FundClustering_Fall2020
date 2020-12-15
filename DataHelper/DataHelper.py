# Data Helper

from .DataMaker import DataMaker
from .DataWriter import DataWriter
import DataHelper.DataReader as DataReader
import DataHelper.DataCatcher as DataCatcher


def get_data_reader(source='sql', **kwargs):

    reader = DataReader._DATA_READERS[source.lower()].instance(**kwargs)

    return reader


def get_data_catcher(source='sql', model='classic', **kwargs):

    catcher = DataCatcher._DATA_CATCHERS[(model.lower(), source.lower())].instance(**kwargs)

    return catcher


def get_data_writer(**kwargs):
    return DataWriter(**kwargs)


def get_data_maker(data_name=''):
    return DataMaker(data_name)
