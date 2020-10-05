from HoldingDataClustering import HoldingDataKMeanClustering
import time

st = time.time()

class Logger:

    def dump(self, a, *args, **kwargs):
        print('\t-> LOG:', a)
        for a in args:
            print(a)
        for x in kwargs:
            print(kwargs[x])
        print(11*'*')


print('** Start')
model = HoldingDataKMeanClustering()

model.load_raw_data(2019)

model.set_up()

sup = time.time()

print("** Set up in {}".format(sup-st))

model.fit(log=Logger())

print("** Fit in {}".format(time.time()-sup))
