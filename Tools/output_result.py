
import numpy as np
import pandas as pd

# Local imports
from Tools import labelling

def output_result_firstlayer(clustering_year, label, features, mrnstar_data, cumul_returns, returns, asset_type, fundno_ticker, save_result = False, loc = None):
    """ output result helper function for first layer clustering """

    fund_ctgy = {mrnstar_data.iloc[j, :]['crsp_fundno']: mrnstar_data.iloc[j, :]['lipper_class_name'] for j in range(len(mrnstar_data))}
    cluster_label = labelling.label_cluster(label, features)
    sharpe_rank, abret_rank = labelling.get_sharpe_ret(cumul_returns, returns, label)
    df = pd.DataFrame(columns=['Fund.No', 'Ticker', 'Cluster'] + asset_type + ['Mstar Category',
                            'Cluster Category', 'sharpe_ratio', 'absolute_return', 'absolute_return_val'])
    df['Fund.No'] = np.array(features.index)
    df['Ticker'] = df['Fund.No'].apply(lambda x: fundno_ticker[int(x)])
    df['Cluster'] = label
    for ass in asset_type:
        df[ass] = np.array(features[ass])
    df['Mstar Category'] = df['Fund.No'].apply(lambda x: fund_ctgy.get(int(x), ''))
    df['Cluster Category'] = df['Cluster'].apply(lambda x: cluster_label[x])
    df['sharpe_ratio'] = df['Fund.No'].apply(lambda x: sharpe_rank[str(x)])
    df['absolute_return'] = df['Fund.No'].apply(lambda x: abret_rank[str(x)][0])
    df['absolute_return_val'] = df['Fund.No'].apply(lambda x: abret_rank[str(x)][1])

    if save_result == True and loc:
        df.to_csv(f'{loc}/cluster_result_{clustering_year}.csv', index=False)
        print('Successfully saved the clustering output!')

    return df


def output_result_secondlayer(clustering_year, subcluster_dict, save_result=False, loc=None):
    """ output result helper function for second layer clustering """

    df = pd.DataFrame.from_dict(subcluster_dict, orient='index', columns=['Cluster', 'Subcluster'])
    df = df.reset_index().rename(columns={"index": "Fund.No"})

    if save_result == True and loc:
        df.to_csv(f'{loc}/cluster_result_withsub_simple_{clustering_year}.csv', index=False)
        print('Successfully saved the subclustering output!')

    return df


def output_result_one_main_cluster(clustering_year, main_cluster, subcluster_dict, save_result=False, loc=None):
    """ output result helper function for one main cluster """

    df = pd.DataFrame.from_dict(subcluster_dict, orient='index', columns=['Subcluster'])
    df = df.reset_index().rename(columns={"index": "Fund.No"})

    if save_result == True and loc:
        df.to_csv(f'{loc}/cluster_{main_cluster}_result_withsub_simple_{clustering_year}.csv', index=False)
        print(f'Successfully saved the subclustering {main_cluster} output!')

    return df


def output_result_two_layer(clustering_year, first_layer_result, subcluster_dict, first_layer_label, save_result_method=False, **kwargs):
    """ output result helper function for two layer clustering

    Input:
        - clustering_year : int
        - first_layer_result : result of the first first_layer
        - subcluster_dict : result of the subclustering
        - first_layer_label : label of first_layer
        - save_result_method :
            * if True : just return the results
            * if 'csv' : save into a csv file
            * if 'sql' : save into a SQL table
    Optional:
        - loc: path to save csv file
        - username, password, secrets_dir: log in to connect to SQL. None if not defined
    """

    df = first_layer_result
    if len(subcluster_dict) != len(first_layer_label):
        raise ValueError('The subclustering for each cluster is not finished.')
    df.insert(int(np.where(df.columns == 'Cluster')[0][0] + 1), 'Subcluster', np.ones(len(df)))
    df['Subcluster'] = df['Fund.No'].apply(lambda x: subcluster_dict[str(x)])

    if save_result == 'csv':

        loc = kwargs.get('loc', None)
        df.to_csv(f'{loc}/cluster_result_withsub_{clustering_year}.csv', index=False)

        print('Successfully saved the clustering and subclustering output in CSV files!')

    elif save_result_method == 'sql':

        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        secrets_dir = kwargs.get('secrets_dir', None)

        df.columns = ['fundNo', 'main_cluster', 'sub_cluster']

        writer = DataHelper.get_data_output_writer(secrets_dir, username, password)
        writer.update_raw_data(df)

        print('Successfully saved the clustering and subclustering output in the SQL table!')

    return df
