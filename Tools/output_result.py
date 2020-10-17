
from Tools import labelling
import numpy as np
import pandas as pd


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


def output_result_secondlayer():
    # will update later
    pass