import matplotlib.pyplot as plt
import numpy as np

def cluster_holding_asset_distribution_boxplot(asset, label, k, asset_type):
    """
    Boxplot of holding asset distribution of each cluster.

    TODO: docstring of this function
    """

    width = 20
    height = ((k//10)+1)*15
    plt.figure(figsize=(width, height))

    for i in range(1, k+1):
        plt.subplot(int(np.ceil(k/4)), 4, i)
        data = [asset.loc[asset.index[label == i-1], :][col] for col in asset_type]
        plt.boxplot(data)
        plt.xlabel(asset_type)
        plt.title(f'cluster_{i-1} with {sum(label==i-1)} components')

    plt.show()
