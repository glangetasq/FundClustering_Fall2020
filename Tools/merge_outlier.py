import numpy as np

def merge_outlier(label, data_nostd, log=None):
    """
    Merge outlier clusters (n<10) into related clusters.

    TODO: docstring of this function
    """

    n = len(np.unique(label))
    centers = {}
    for i in range(n):
        centers[i] = data_nostd[label==i].median(axis=0)

    for i in range(n):
        if sum(label == i) <= 10:
            mn = float('inf')
            res = None
            for j in range(n):
                if j == i:
                    continue
                if j in centers:
                    distance = (centers[i] - centers[j]).abs().sum()
                else:
                    continue
                if all(np.argsort(np.floor(centers[i])) == np.argsort(np.floor(centers[j]))) and distance < mn:
                    mn = distance
                    res = j
            if res is not None:
                label = np.where(label == i, res, label)
                del centers[i]
                if log:
                    log.dump('Description', f'cluster{i} get merged into cluster{res}')

    new_n = len(np.unique(label))
    numbers = sorted(np.unique(label), reverse=True)
    l = 0
    for i in range(new_n):
        if i not in numbers:
            label = np.where(label == numbers[l], i, label)
            l += 1

    return label
