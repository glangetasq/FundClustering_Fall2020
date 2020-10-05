from HoldingDataClustering import HoldingDataKMeanClustering
import time

model = HoldingDataKMeanClustering()

start_time = time.time()

model.load_raw_data(2019)
model.set_up()

set_up_time = time.time()
print(f">>> Set up finished in {set_up_time-start_time}.")

model.fit()

print(f">>> Fit finished in {time.time()-set_up_time}.")
