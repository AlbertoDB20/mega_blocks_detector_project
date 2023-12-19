# use this for test python code
import os
import cv2

path = "/Users/alberto/Desktop/prj/data/images/val"
file = "rbw_my_img_0__frame_50.jpg"

with open(os.path.join(path, file), 'rb') as f:
    check_chars = f.read()[-2:]
if check_chars != b'\xff\xd9':
    print('Not complete image')
else:
    imrgb = cv2.imread(os.path.join(path, file), 1)