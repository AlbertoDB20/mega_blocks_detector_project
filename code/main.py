'''
Trainig from a python script

YOLOv8n --> lightest one, but it is also possible to chose another version of YOLOv8

pip install ultralytics


'''


from ultralytics import YOLO

# Load a model
model = YOLO ("yolov8n.yaml")       # build new model from scratch

# Use the model
result = model.train(data = "/Users/alberto/ROBOTICS/code/config.yaml", epochs=1)       # train the model
