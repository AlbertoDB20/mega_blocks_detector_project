from ultralytics import YOLO

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"  

# path to last.pt file to refer for resume training procedure
path_last_model = path_to_project_folder + "/runs/detect/train12/weights/last.pt"


# Load a model
model = YOLO(path_last_model)

# Resume training 
results = model.train(resume=True)