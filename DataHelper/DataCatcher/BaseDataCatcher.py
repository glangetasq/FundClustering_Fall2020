
import pandas as pd


class BaseDataCatcher:


    def __init__(self, reader):

        self.reader = reader
        self.data = list() # self.data[k] = data for (k+1)th layer


    def _append_previous_clusters(self, k, clusters):
        """
        Input:
            - k: (k+1)th layer we want to append the results to its data.
            - clusters: dict, such as { fundNo: (cluster1, cluster2, ...) }
        """

        if k == 0:
            raise ValueError("Not supposed to append empty results: k = 0.")

        m_clusters = k # There are supposed to be k already computed cluster layers.

        columns = [ f"cluster_{k+1}" for k in range(m_clusters) ]

        # The result of each layers are assumed to be dictionaries, get DataFrame from dict
        clusters = pd.DataFrame.from_dict(clusters, orient='index', columns=columns)

        # Merge past cluster layer results to features of next layer
        self.data[k].join(clusters)
