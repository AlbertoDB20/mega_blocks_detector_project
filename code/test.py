# use this for test python code
import os
import cv2

path = "/Users/alberto/ROBOTICS/autovelox_detector_project/data/images/test"
file = "rbw_img_3.jpeg"

with open(os.path.join(path, file), 'rb') as f:
    check_chars = f.read()[-2:]
if check_chars != b'\xff\xd9':
    print('Not complete image')
else:
    imrgb = cv2.imread(os.path.join(path, file), 1)