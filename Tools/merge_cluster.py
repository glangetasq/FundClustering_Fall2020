import numpy as np

def merge_cluster(feature, label, k, identical_asset=3, argsort=False):
    """
    Merge similar clusters.

    Similar cluster are defined by having cluster centers that are really close
    to each other.

    TODO: docstring of this function
    """

    clust_centers = []

    for i in range(k):
        similar = False
        df = feature[label == i]
        center = df.median(axis=0)
        for c in clust_centers:
            if argsort:
                criteria = (sum((center - c).abs() <= 10) >= identical_asset and max((center - c).abs()) <= 20) or \
            (all(np.argsort(np.floor(center)) == np.argsort(np.floor(c))) and all((center - c).abs() <= 25))
            else:
                criteria = sum((center - c).abs() <= 10) >= identical_asset and max((center - c).abs()) <= 20

            if criteria:
                similar = True
                break
        if not similar:
            clust_centers.append(center)

    clust_centers = np.array(clust_centers)

    return np.unique(clust_centers, axis=0)
