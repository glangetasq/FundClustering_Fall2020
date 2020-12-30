
import numpy as np

def label_cluster(l, data_nostd):
    k = len(np.unique(l))
    labelling = {}
    ref = {0:data_nostd.columns[0],
            1:data_nostd.columns[1],
            2:data_nostd.columns[2],
            3:data_nostd.columns[3]}
    for i in range(k):
        index = data_nostd[l==i].median(axis=0)
        if index[0] <= -20:
            if index[1] >= 80:
                labelling[i] = 'Leveraged ' + ref[1] + ' group'
            elif index[2] >= 80:
                labelling[i] = 'Leveraged ' + ref[2] + ' group'
            elif index[3] >= 80:
                labelling[i] = 'Leveraged ' + ref[3] + ' group'
            else:
                labelling[i] = 'Leveraged mixed group'
        elif max(index) >= 80:
            labelling[i] = np.argmax(index) + ' driven group'
        elif sum(list(map(lambda x: x >= 10, index))) >= 3:
            labelling[i] = 'Deversified group'
        elif sum(list(map(lambda x: x >= 25, index))) >= 2:
            if index[0] >= 25 and index[1] >= 25:
                labelling[i] = ref[0] + ' ' + ref[1] + ' mixed group'
            elif index[0] >= 25 and index[2] >= 25:
                labelling[i] = ref[0] + ' ' + ref[2] + ' mixed group'
            elif index[0] >= 25 and index[3] >= 25:
                labelling[i] = ref[0] + ' ' + ref[3] + ' mixed group'
            elif index[1] >= 25 and index[2] >= 25:
                labelling[i] = ref[1] + ' ' + ref[2] + ' mixed group'
            elif index[1] >= 25 and index[3] >= 25:
                labelling[i] = ref[1] + ' ' + ref[3] + ' mixed group'
            elif index[2] >= 25 and index[3] >= 25:
                labelling[i] = ref[2] + ' ' + ref[3] + ' mixed group'
        else:
            labelling[i] = 'Mixed investment group'
            
    return labelling
