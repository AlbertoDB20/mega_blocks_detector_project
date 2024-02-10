##
# @mainpage Predict with fine-tuned model
#
# @section Description
# An example Python program demonstrating how to use predict function for
# generating inference on image with fine-tuned model 
#
# @section Notes
# - use best.pt model that can be found into runs/detect/train/weight folder if you want to use weights for best performances detection 
#


##
# @file custom_model.py
# @brief Using the best.pt model fine-tuned model, this script allow making predictions given an image.
# @date   10/11/2023
# @author Alberto Dal Bosco
#

# Imports
from ultralytics import YOLO
import cv2
import os


# Global Constants
## ID of megablocks
id0 = "X1-Y1-Z2"
id1 = 'X1-Y2-Z1'
id2 = 'X1-Y2-Z2'
id3 = 'X1-Y2-Z2-CHAMFER'
id4 = 'X1-Y2-Z2-TWINFILLET'
id5 = 'X1-Y3-Z2'
id6 = 'X1-Y3-Z2-FILLET'
id7 = 'X1-Y4-Z1'
id8 = 'X1-Y4-Z2'
id9 = 'X2-Y2-Z2'
id10 = 'X2-Y2-Z2-FILLET'

## switch to absolute value bb outputs
ABSOLUTE_VALUE = True   # if True -->  xc, yc, w, h are expressed in pixel, otherwise are relative.

class bb:
    """! The bounding box base class.
    Defines the base class for all the object detected
    """

    def __init__(self, ID, prec, xc, yc, w, h):
        """! The bounding box base class initializer.
        @param ID  The ID of the object detected.
        @param prec  The precision of the object detected.
        @param xc  The x coordinate of the center of the bb of the object detected.
        @param yc  The y coordinate of the center of the bb of the object detected.
        @param w  The width of the bb of the object detected.
        @param h  The height of the bb of the object detected.
        @return  None
        """
        self.ID = ID
        self.prec = prec
        self.xc = xc
        self.yc = yc
        self.w = w
        self.h = h

    def convert_id_to_num(self):
        """! Function that covert litteral IDs to numbers.
        @return num numerical ID or print error
        """
        if self.ID == id0:
            return 0
        elif self.ID == id1:
            return 1
        elif self.ID == id2:
            return 2
        elif self.ID == id3:
            return 3
        elif self.ID == id4:
            return 4
        elif self.ID == id5:
            return 5
        elif self.ID == id6:
            return 6
        elif self.ID == id7:
            return 7
        elif self.ID == id8:
            return 8
        elif self.ID == id9:
            return 9
        elif self.ID == id10:
            return 10
        else:
            print("ERROR: no matching of ID")
            exit()

    def convert_num_to_id(self):
        """! Function that covert numbers to litteral IDs.
        @return string ID or print error
        """
        if self.ID == 0:
            return id0
        elif self.ID == 1:
            return id1
        elif self.ID == 2:
            return id2
        elif self.ID == 3:
            return id3
        elif self.ID == 4:
            return id4
        elif self.ID == 5:
            return id5
        elif self.ID == 6:
            return id6
        elif self.ID == 7:
            return id7
        elif self.ID == 8:
            return id8
        elif self.ID == 9:
            return id9
        elif self.ID == 10:
            return id10
        else:
            print("ERROR: no matching of number")
            exit()

    def print(self):
        """! function to print on stdout bounding box information.
        @return None
        """
        print("\nBB")
        print("   class:     " + str(int(self.ID)))
        print("   precision: " + str(self.prec) + " %")
        if ABSOLUTE_VALUE:
            print("   (xc, yc): (" + str(int(self.xc)) + "," + str(int(self.yc)) + ")")
            print("   (w, h):   (" + str(int(self.w)) + "," + str(int(self.h)) + ")")
        else:
            print("   (xc, yc): (" + str(self.xc) + "," + str(self.yc) + ")")
            print("   (w, h):   (" + str(self.w) + "," + str(self.h) + ")")
        print("\n")


## define path useful for testing 
path_to_my_image = '/Users/alberto/Desktop/img_from_alex/img3.jpg'

# get the current working directory
current_working_directory = os.getcwd()

# path_model
path_model = current_working_directory + "/runs/detect/train/weights/best.pt"

# Load a pre-trained YOLOv8n model (choose the best.pt file to have best performances)
model = YOLO (path_model)



def make_prediction(image):
    """! The function that make effective prediction given the image based on the yolo v8 fine-tuned model create
    @brief This function computes size of given image and then uses yolo v8 model.predict pre-defined function that run inference on the source, to which I pass following values defined by real world experience:
                * source = path --> takes that specific video of image path.
                * source = 1    --> use the webcam of the pc, 0 to the external camera
                * show = True   --> shows webcam view
                * conf = 0.3    --> object confidence threshold for detection
                * save = True   --> save predicted images and videos)
                * iou_thres = 0.7   --> intersection over union threshold value
            Set to True or false variable ABSOLUTE_VALUE if you want to have relative or absolute measurement
    
            N.B.:  each bb constains following information:
            * ID --> from 0 to 10
            * prec --> from 0 to 100 (it is a percentage)
            * xc --> from 0 to x size of image (x coordinate of center of bounding box with absolute coordinate)
            * yc --> from 0 to y size of image (y coordinate of center of bounding box with absolute coordinate)
            * w --> from 0 to x size of bounding box (width of bounding box with absolute coordinate)
            * h --> from 0 to y size of bounding box (height of bounding box with absolute coordinate)

    @param image The openCV image from the camera view. This has to be .jpg extentions
    @return bbs It's a list of bounding box [bb0, bb1, .... , bbn]
    
    """
    # creating a object
    height, width, channel = image.shape
    h = int(height)
    w = int(width)

    results = model.predict(source=image, imgsz=(h,w), show=True, conf=0.85, save=True)   
    bbs = []  
    i = 0
    for result in results:
        print("\n")
        boxes = result.boxes.numpy()   # Boxes object for bbox outputs
        for box in boxes:
            cls = box.cls
            confidence = box.conf
            values = box.xywh
            prec = int(confidence[0]*100)
            if ABSOLUTE_VALUE:
                bbs.append(bb(cls, prec, values[0][0], values[0][1], values[0][2], values[0][3]))
            else:
                bbs.append(bb(cls, prec, values[0][0]/w, values[0][1]/h, values[0][2]/w, values[0][3]/h))
            bbs[i].print()
            i += 1
    return bbs


## necessary to have an openCV image to input to make_prediction
#!!! img_in_cv2_format = cv2.imread(path_to_my_image)
## test make_prediction function.
#!!! make_prediction(img_in_cv2_format)
