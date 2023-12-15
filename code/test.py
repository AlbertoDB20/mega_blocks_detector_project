# use this for test python code
import os
import cv2

path = "/Users/alberto/ROBOTICS/autovelox_detector_project/"
file = "my_img_0__frame_150_jpeg.rf.068edbb4669b4e4eed834d0688c4407a.jpg"

with open(os.path.join(path, file), 'rb') as f:
    check_chars = f.read()[-2:]
if check_chars != b'\xff\xd9':
    print('Not complete image')
else:
    imrgb = cv2.imread(os.path.join(path, file), 1)