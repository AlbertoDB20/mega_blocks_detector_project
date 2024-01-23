'''
Custom trained ultralytics YOLO v8 model to be run to detect live inference on webcam
Refer to the model trained in fine_tuning.py script. 
From that training, it is possible to choose best.pt or last.pt model in path
        /__project_name__/runs/detect/train__num__/weights


'''


from ultralytics import YOLO
import cv2

# ID of megablocks
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

ABSOLUTE_VALUE = True                   # if True -->  xc, yc, w, h are expressed in pixel, otherwise are relative.  

class bb:
    def __init__(self, ID, prec, xc, yc, w, h):
        self.ID = ID
        self.prec = prec
        self.xc = xc
        self.yc = yc
        self.w = w
        self.h = h

    def convert_id_to_num(self):
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
            print("ERROR: no matching of id")
            exit()

    def print(self):
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



# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/Desktop"       # for the other good model: "/Users/alberto/ROBOTICS/autovelox_detector_project" 

# path to best.pt file to refer for prediction   --> CHANGE TRAIN# FOLDER
path_best_model = path_to_project_folder + "/FINAL_RUNS/detect/train/weights/best.pt"             # for the other good model "/runs/detect/final_training/best.pt"

path_to_video = 'insert here'
path_to_my_image = '/Users/alberto/ROBOTICS/autovelox_detector_project/assigns/my_photo/scene0.jpg'
path_to_test_image = '/Users/alberto/ROBOTICS/autovelox_detector_project/data/images/test'


# Load a pre-trained YOLOv8n model (choose the best.pt file)
model = YOLO (path_best_model)       # build new model from scratch



'''
This is the function to make the prediction given a cv2 image.
    input: 
        * cv2.image of zed camera
        * other possible parameters

    output:   list of class of bb    [bb0, bb1, .... , bbn].
                |
                '--------> this list has length n, where n is the number of bb in the image passed to the function.
                '--------> bb is a class (structured type) that contains in order the following value: ID, xc, yc, w, h
        
        N.B.:  each bb constains following information:
            * ID --> from 0 to 10
            * prec --> from 0 to 100 (it is a percentage)
            * xc --> from 0 to x size of image (x coordinate of center of bounding box with absolute coordinate)
            * yc --> from 0 to y size of image (y coordinate of center of bounding box with absolute coordinate)
            * w --> from 0 to x size of bounding box (width of bounding box with absolute coordinate)
            * h --> from 0 to y size of bounding box (height of bounding box with absolute coordinate)

        N.B.:   print(type(list_of_bb[0]))        --->        <class '__main__.bb'>

This function computes size of given image and then uses yolo v8 model.predict pre-defined function that run inference on the source, 
to which I pass following values defined by real world experience:
    * source = path --> takes that specific video of image path.
    * source = 1    --> use the webcam of the pc, 0 to the external camera
    * show = True   --> shows webcam view
    * conf = 0.3    --> object confidence threshold for detection
    * save = True   --> save predicted images and videos)
    * iou_thres = 0.7   --> intersection over union threshold value         #TODO: check this!!!

Set to True or false variable ABSOLUTE_VALUE if you want to have relative or absolute measurement

'''


def make_prediction(image):
    # creating a object
    img = cv2.imread(image)
    height, width, c = img.shape
    h = int(height)
    w = int(width)

    results = model.predict(source=image, show=True, conf=0.6, save=False)   
    bbs = []  
    i = 0
    for result in results:
        print("\n")
        boxes = result.boxes.numpy()  # Boxes object for bbox outputs
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

  

list_of_bb = make_prediction(path_to_my_image)





# TODO: intersection over union in case of Bounding box overlapping
        