'''

   ________________________________________FIRST SCRIPT TO BE EXECUTED______________________________________


   PYTHON SCRIPTS TO CREATE ALL THE FOLDER NECESSARY FOR THE PROJECTS
   This script made all us. 
   It creates all the necessary folder for the project, each of one contains a personal README.md file.
   PAY ATTENTION:
    --> Modify only the path_to_project_folder, selecting the folder in which you commonly store the project 
    --> then it is automatic the creation of the folder
   
   If you have just images for the datasets, save it in the images folder.
   Moreover, if you have video in which extracting frames, save it in path_to_videos_folder according to their extensions.

   FOLDER STRUCTURE:

   PROJECT
      assigns  --> contain Sebe dataset (to be modified)
      data     --> contain all the data (images and labels)
      code     --> contain python scripts, model, configuration file 
      Models   --> contain 3D stl and obj file 
      runs     --> contain train model, statistics, weights, results, ...

   This script create data and code folder with all the subsolder needed by the other python programs
   assigns, models, folder must be add by us
   runs folder it is created automatically by fine-tuning.py script

   AFTER:
   JSONtoYOLO script to take all the images and labels from Sebe dataset and rename/convert/move into data folder


   author: Alberto Dal Bosco 
   date: 22/11/2023
   
'''


import os

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project" 

# DO NOT MODIFY THESE
path_to_data_folder = path_to_project_folder + "/data"
path_to_code_folder = path_to_project_folder + "/code"

path_to_images_folder = path_to_data_folder + "/images"
path_to_labels_folder = path_to_data_folder + "/labels"
path_to_videos_folder = path_to_data_folder + "/videos"

path_to_images_train_folder = path_to_images_folder + "/train"
path_to_images_val_folder = path_to_images_folder + "/val"
path_to_images_test_folder = path_to_images_folder + "/test"

path_to_labels_train_folder = path_to_labels_folder + "/train"
path_to_labels_val_folder = path_to_labels_folder + "/val"
path_to_labels_test_folder = path_to_labels_folder + "/test"

path_to_videos_MOV_folder = path_to_videos_folder + "/videos_MOV"
path_to_videos_MP4_folder = path_to_videos_folder + "/videos_MP4"


# Content of README files
string1 = "PROJECT FOLDER\nThis is the root directory of the project"
string2 = "DATA FOLDER\nThis is the root directory for all the data in your datasets"
string3 = "CODE FOLDER\nThis is the root directory for all the code in your datasets, that could be python scripts, config.yaml, shell files, ..."
string4 = "IMAGES FOLDER\nThis is the folder in which saving all the images of your personal datasets, then they will be well organized in the sub-folder train, val, testing.\nThis is not a user commitment, because there is a specific python scripts which rights for us."
string5 = "LABELS FOLDER\nThis is the labels folder.\nHere you have to save all the labels created with a tool on the web or by your hand.\nI really suggest CVAT online tool because it is very easy to use.\nThe labels has to be divided into the three sub folder, but also in this case is not a user commitment"
string6 = "VIDEOS FOLDER\nThis is the videos folder.\nHere you have to select the folder in which saving your video, according the video extension"
string7 = "TRAIN FOLDER\nThis folder will have the 70'%' of all the images in the datasets. This images will be used to fine-tuning the pre-trained model, or to train our personal model."
string8 = "VAL FOLDER\nThis folder will have the 15'%' of all the images in the datasets. This images will be used to validate the pre-trained model or our personal model."
string9 = "TEST FOLDER\nThis folder will have the 15'%' of all the images in the datasets. This images will be used to test the pre-trained model or our personal model."
string10 = "TRAIN LABELS FOLDER\nThis folder will contain the respective labels of the images in train folder"
string11 = "VAL LABELS FOLDER\nThis folder will contain the respective labels of the images in val folder"
string12 = "TEST LABELS FOLDER\nThis folder will contain the respective labels of the images in test folder"
string13 = "MOV VIDEOS FOLDER\nSave in this folder all the .MOV extended video, then these will be elaborated by a python scripts and tranformed into MP4 files, saved in MP4 videos folder.\nThis passage is necessary because the script for framing do not accept .MOV videos"
string14 = "MP4 VIDEOS FOLDER\nSave in this folder all the .mp4 extended video, then these will be elaborated by a python scripts and tranformed to a sequence of frame, saved in images folder"




# function to create README.md given the path
def create_readme(path, readme_content):
   # Scrivi il contenuto nel file README.txt
   readme_path = os.path.join(path, 'README.md')
   if os.path.isfile(readme_path):
      return
   else:
      with open(readme_path, 'w') as readme_file:
         readme_file.write(readme_content)




# I create all the necessary folder for the project
try: 
   if not os.path.exists(path_to_project_folder):
      os.makedirs(path_to_project_folder)
   create_readme(path_to_project_folder, string1)
except OSError:
   print("ERROR in creating directory for {path_to_project_folder}")

try: 
   if not os.path.exists(path_to_data_folder):
      os.makedirs(path_to_data_folder)
   create_readme(path_to_data_folder, string2)
except OSError:
   print("ERROR in creating directory for {path_to_data_folder}")

try: 
   if not os.path.exists(path_to_code_folder):
      os.makedirs(path_to_code_folder)
   create_readme(path_to_code_folder, string3)
except OSError:
   print("ERROR in creating directory for {path_to_code_folder}")

try: 
   if not os.path.exists(path_to_images_folder):
      os.makedirs(path_to_images_folder)
   create_readme(path_to_images_folder, string4)
except OSError:
   print("ERROR in creating directory for {path_to_images_folder}")

try: 
   if not os.path.exists(path_to_labels_folder):
      os.makedirs(path_to_labels_folder)
   create_readme(path_to_labels_folder, string5)
except OSError:
   print("ERROR in creating directory for {path_to_labels_folder}")

try: 
   if not os.path.exists(path_to_videos_folder):
      os.makedirs(path_to_videos_folder)
   create_readme(path_to_videos_folder, string6)
except OSError:
   print("ERROR in creating directory for {path_to_videos_folder}")

try: 
   if not os.path.exists(path_to_images_train_folder):
      os.makedirs(path_to_images_train_folder)
   create_readme(path_to_images_train_folder, string7)
except OSError:
   print("ERROR in creating directory for {path_to_images_train_folder}")

try: 
   if not os.path.exists(path_to_images_val_folder):
      os.makedirs(path_to_images_val_folder)
   create_readme(path_to_images_val_folder, string8)
except OSError:
   print("ERROR in creating directory for {path_to_images_val_folder}")

try: 
   if not os.path.exists(path_to_images_test_folder):
      os.makedirs(path_to_images_test_folder)
   create_readme(path_to_images_test_folder, string9)
except OSError:
   print("ERROR in creating directory for {path_to_images_test_folder}")

try: 
   if not os.path.exists(path_to_labels_train_folder):
      os.makedirs(path_to_labels_train_folder)
   create_readme(path_to_labels_train_folder, string10)
except OSError:
   print("ERROR in creating directory for {path_to_labels_train_folder}")

try: 
   if not os.path.exists(path_to_labels_val_folder):
      os.makedirs(path_to_labels_val_folder)
   create_readme(path_to_labels_val_folder, string11)
except OSError:
   print("ERROR in creating directory for {path_to_labels_val_folder}")

try: 
   if not os.path.exists(path_to_labels_test_folder):
      os.makedirs(path_to_labels_test_folder)
   create_readme(path_to_labels_test_folder, string12)
except OSError:
   print("ERROR in creating directory for {path_to_labels_test_folder}")

try: 
   if not os.path.exists(path_to_videos_MOV_folder):
      os.makedirs(path_to_videos_MOV_folder)
   create_readme(path_to_videos_MOV_folder, string13)
except OSError:
   print("ERROR in creating directory for {path_to_videos_MOV_folder}")

try: 
   if not os.path.exists(path_to_videos_MP4_folder):
      os.makedirs(path_to_videos_MP4_folder)
   create_readme(path_to_videos_MP4_folder, string14)
except OSError:
   print("ERROR in creating directory for {path_to_videos_MP4_folder}")




