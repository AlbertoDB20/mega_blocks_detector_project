'''
Trainig from a python script

YOLOv8n --> lightest one, but it is also possible to chose another version of YOLOv8

pip install ultralytics

FROM REFERENCE

    from ultralytics import YOLO

    # Load a YOLOv8 model from a pre-trained weights file
    model = YOLO('yolov8n.pt')

    # Run MODE mode using the custom arguments ARGS (guess TASK)
    model.MODE(ARGS)


Where:

TASK (optional) is one of (detect, segment, classify, pose)
MODE (required) is one of (train, val, predict, export, track)
ARGS (optional) are arg=value pairs like imgsz=640 that override defaults.
Default ARG values are defined on this page from the cfg/defaults.yaml file.


'''


from ultralytics import YOLO
import torch

print("AVAILABLE MPS: ", torch.backends.mps.is_available())

# Load a model
model = YOLO ("yolov8n.yaml")       # build new model from scratch

# Use the model
result = model.train(data = "/Users/alberto/ROBOTICS/autovelox_detector_project/code/config.yaml", epochs=1, device="mps")       # train the model


