'''
Custom trained ultralytics YOLO v8 model to be run to detect live inference on webcam
Refer to the model trained in fine_tuning.py script. 
From that training, it is possible to choose best.pt or last.pt model in path
        /__project_name__/runs/detect/train__num__/weights


'''


from ultralytics import YOLO

# Load a pre-trained YOLOv8n model
model = YOLO ('best.pt')       # build new model from scratch

# Run inference on the source  (PREDICT MODE)
results = model(source=1, show=True, conf=0.3, save=True)       
    # source = 1    --> use the webcam of the pc
    # show = True   --> shows webcam view
    # conf = 0.3    --> object confidence threshold for detection
    # save = True   --> save predicted images and videos

# export the model 
model.export(format='onnx')         # TODO: which is the correct format for our ROS project?

