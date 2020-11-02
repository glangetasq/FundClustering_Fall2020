""" Result output helper functions for second layer clustering main class """

import matplotlib.pyplot as plt
import numpy as np


def organize_label(subcluster_label):
    label = subcluster_label
    label_set = set(label)
    number_of_cluster = len(label_set)
    for i in range(number_of_cluster):
        if i in label_set:
            continue
        else:
            mx = max(label_set)
            label = np.where(label==mx, i, label)
            label_set.add(i)
            label_set.remove(mx)

    return label


def plot_sub_result(subcluster_k, fundnos, subcluster_label, cumret_data):
    k = subcluster_k
    width = 16
    height = ((k//10)+1)*15
    plt.figure(figsize=(width, height))
    for i in range(1, k+1):
        plt.subplot(int(np.ceil(k/4)), 4, i)
        for fund in fundnos[subcluster_label==(i-1)]:
            plt.plot(cumret_data[fund])
        plt.title(f'Cluster_{i-1} with {sum(subcluster_label==(i-1))} components')
    plt.show()
