from ultralytics import YOLO

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
#path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"  
path_to_project_folder = "/Users/alberto/Desktop/102_200_epochs_samuele_ferraglio"  

# path to last.pt file to refer for resume training procedure
path_last_model = path_to_project_folder + "/runs/detect/train/weights/last.pt"


# Load a model
model = YOLO(path_last_model)

# Resume training 
model.train(data="/Users/alberto/ROBOTICS/autovelox_detector_project/code/config.yaml", resume=True, augment=False, fraction=1.0, seed=0,scale=0.5)