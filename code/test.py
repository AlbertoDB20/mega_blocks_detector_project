from tqdm import tqdm
import os
from time import sleep

pbar = tqdm(os.listdir('/Users/alberto/ROBOTICS/autovelox_detector_project/assigns'))
for char in pbar:
    sleep(0.25)

n_folder = int(os.listdir('/Users/alberto/ROBOTICS/autovelox_detector_project/assigns').count)
print(n_folder)
print(type(n_folder))