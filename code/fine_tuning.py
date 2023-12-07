'''
Script for fine-tuning in python using ultralytics YOLO v8 pre-trained model
We choose YOLOv8n because is the lightest one, but it is also possible to chose another version of YOLOv8

TO DO BEFORE COMPILING:
pip install ultralytics
pip install torch

FROM REFERENCE we have:

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

I also check if MPS is available to be sure to use Apple Neural Engine for M1 processor.
    [ Apple's Neural Engine (ANE) is the marketing name for a group of specialized 
      cores functioning as a neural processing unit (NPU) dedicated to the acceleration 
      of artificial intelligence operations and machine learning tasks. ]
    source: Apple

    

author: Alberto Dal Bosco
date: 1/12/2023 

'''


from ultralytics import YOLO
import torch

print("AVAILABLE MPS: ", torch.backends.mps.is_available())

# Load a model
model = YOLO ("yolov8n.yaml")       # build new model from scratch

# Use the model
result = model.train(data = "/Users/alberto/ROBOTICS/autovelox_detector_project/code/config.yaml", epochs=1, device="mps")       # train the model

