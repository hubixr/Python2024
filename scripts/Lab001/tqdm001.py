import tqdm
import time
import random

# for i in range(100):
#     time.sleep(random.random())
#     print(i)

for i in tqdm.tqdm(range(100)):
    time.sleep(random.random())