# Data Helper

import pandas as pd
from .DataMaker import DataMaker
import DataHelper.DataWriter as DataWriter
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



def output_clustering_results(source, result_dict, **kwargs):

    writer = DataWriter._DATA_WRITERS[source.lower()](**kwargs)

    # Convert result_dict to dataframe
    # TODO: only assuming 2-layer models currently.
    clusters = pd.DataFrame.from_dict(result_dict)
    clusters.columns = ['main_cluster', 'sub_cluster']
    clusters = clusters.reset_index().rename(columns={'index':'fundNo'})

    if source.lower() == 'csv':
        assert( 'path' in kwargs )
    elif source.lower() == 'sql':
        assert( 'db_name' in kwargs and 'table_name' in kwargs )

    writer.update_raw_data(result_dict, **kwargs)
