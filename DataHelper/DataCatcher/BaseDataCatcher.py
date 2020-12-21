
import pandas as pd


class BaseDataCatcher:


    def __init__(self, reader):

        self._iterator = None
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


    def _pack_data(self):
        # Must be an iterator
        raise NotImplementedError("DataCatcher subclasses must implement _pack_data.")


    def unpack_data(self, keys):
        """
        The iterator (implemented by children classes) yields the data for each layer in succesion
        """

        if self._iterator is None:
            self._iterator = self._pack_data()

        try:
            data_dict = next(self._iterator)
        except StopIteration:
            self._iterator = self._pack_data()
            data_dict = next(self._iterator)

        return tuple(data_dict.get(k, None) for k in keys)
