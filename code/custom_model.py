'''
Custom trained ultralytics YOLO v8 model to be run to detect live inference on webcam
Refer to the model trained in fine_tuning.py script. 
From that training, it is possible to choose best.pt or last.pt model in path
        /__project_name__/runs/detect/train__num__/weights


'''


from ultralytics import YOLO
import cv2


path_to_model = '/Users/alberto/runs/detect/train6/weights/best.pt'
path_to_video = 'insert here'
path_to_my_image = '/Users/alberto/ROBOTICS/autovelox_detector_project/assigns/my_photo/img7.jpg'
path_to_test_image = '/Users/alberto/ROBOTICS/autovelox_detector_project/data/images/test/img_5.jpeg'

# Load a pre-trained YOLOv8n model
model = YOLO (path_to_model)       # build new model from scratch

# creating a object
image = cv2.imread(path_to_test_image)

h, w, c = image.shape
size = (h, w)

# Run inference on the source  (PREDICT MODE)
results = model.predict(source=path_to_my_image, show=True, conf=0.4, save=True, imgsz = size)       
    # source = path --> takes that specific video of image path.
    # source = 1    --> use the webcam of the pc
    # show = True   --> shows webcam view
    # conf = 0.3    --> object confidence threshold for detection
    # save = True   --> save predicted images and videos


# export the model 
#model.export(format='onnx')         # TODO: which is the correct format for our ROS project?


for result in results:
    print("\n")
    boxes = result.boxes.numpy()  # Boxes object for bbox outputs
    for box in boxes:
        cls = box.cls
        conf = box.conf
        bb = box.xywh
        print("RESULT FOR OBJ CLASS: "+ str(int(cls[0])))
        print("   p: {:.2f} ".format(round(conf[0], 2)))
        print("   C: (" + str(int(bb[0][0])) + "," + str(int(bb[0][1])) + ")")
        print("\n")