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

    AFTER:
    custom_model.py to use the trained model in real environment
        

    author: Alberto Dal Bosco
    date: 1/12/2023 

'''


from ultralytics import YOLO
import torch

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"  

# path to yaml config file
path_config = path_to_project_folder + "/code/config.yaml"


if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyThorch install was not build with MPS enabled")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ and/or you do not have an MPS-enabled device on this machine.")
else:
    mps_device = torch.device("mps")

# Load a model
model = YOLO ("yolov8n.yaml")       # build new model from scratch

# Use the model
result = model.train(data = path_config, epochs=3, imgsz=640, device = mps_device)       # train the model
#model.to(mps_device)       # not convenient
