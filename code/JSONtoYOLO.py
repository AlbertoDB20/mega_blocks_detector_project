# Python program to read
# json file
 
import json
import os
import re
import shutil

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_assigns_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project/assigns"

# path for subfolder: DO NOT MODIFY THIS!
path_to_images = path_to_assigns_folder + "/images"
path_to_txt_labels = path_to_assigns_folder + "/labels"

# useful string
img = "img_"
key = 'obj-0'
subkey = '3d_bbox_pixel_space'                  # I am taking the 3D BB for the image
#subkey = 'bbox'                                # I am taking the 2D BB for the image --> verify!! Is not in YOLO format!

# counter for images and labels files
cont_img = 0
cont_lab = 0

# List to store JSON and images files 
json_files = []
img_files = []



# I create/check the folder
try: 
   if not os.path.exists(path_to_images):
      os.makedirs(path_to_images)
except OSError:
   print("ERROR in creating directory for image")

try: 
   if not os.path.exists(path_to_txt_labels):
      os.makedirs(path_to_txt_labels)
except OSError:
   print("ERROR in creating directory for txt labels")

try: 
   if not os.path.exists(path_to_assigns_folder):
        print("FOLDER READY")
except OSError:
   print("ERROR: no assigns folder found")




def remove_numbers(input_string):
    """
    Remove numbers from the input string.

    Parameters:
    - input_string (str): The input string.

    Returns:
    - str: The string without numbers.
    """
    return ''.join(char for char in input_string if not char.isdigit())



# function to create .txt annotation file in the form:________img_#num_label.txt_________ 
def create_txt_annotation(path_json, path_txt_folder):
    global cont_lab
    new_file_name = img + str(cont_lab) + ".txt"                # img_#num_label.txt

    # Create the new full path for the image in the destination folder
    new_label_path = os.path.join(path_txt_folder, new_file_name)
    
    # Apre il file JSON e carica i dati
    with open(path_json, 'r') as file:
        data = json.load(file)

    # Ora puoi accedere ai dati come desideri. Ad esempio, se il file JSON contiene una chiave 'bbox', puoi fare qualcosa del genere:
    if key in data and subkey in data[key]:
        values = data[key][subkey]
        # Ora puoi lavorare con i dati della bounding box come richiesto nel tuo script 3d_bbox_pixel_space.
        with open(new_label_path, 'w') as annotation_file:
            annotation_file.write(str(values))                                      # TODO: call here a function to create YOLO annotation
    else:
        print("La sottochiave {subkey} non è presente nel file JSON.")
    cont_lab = cont_lab + 1


def save_img(img_file_path, path_to_images):
    global cont_img
    # Modify the file name as desired (e.g., add a prefix)
    new_file_name = img + str(cont_img) + ".jpeg"                # img_#num.jpeg

    # Create the new full path for the image in the destination folder
    new_image_path = os.path.join(path_to_images, new_file_name)

    # Copy the image to the new location with the new name
    shutil.copyfile(img_file_path, new_image_path)
    cont_img = cont_img + 1



# Filter only files with the ".json" extension
for folder_name in os.listdir(path_to_assigns_folder):
    #folder_name_no_number = remove_numbers(folder_name)                    # uncomment this two lines to read also assign2 and assign3 
    #if(folder_name_no_number.startswith("assign")):
    if "assign1" in folder_name:
        folder_path = os.path.join(path_to_assigns_folder, folder_name)
        for scene_name in os.listdir(folder_path):
            if "scene" in scene_name:
                scene_path = os.path.join(folder_path, scene_name)
                print (scene_path)
                for file_name in os.listdir(scene_path):
                    file_path = os.path.join(scene_path, file_name)
                    if file_name.endswith(".json"):
                        json_files.append(file_path)
                        create_txt_annotation(file_path, path_to_txt_labels)
                    if file_name.startswith("view=") and file_name.endswith(".jpeg") and "_vertices" not in file_name and "_depth" not in file_name and "_depth_plane" not in file_name and "_bbox" not in file_name:
                        img_files.append(file_path)
                        save_img(file_path, path_to_images)

#print("FIRST 10 ELEMENT (debug):", json_files[:10])


lj = len(json_files)
li = len(img_files)
if (lj != li):
    print("ERRORE: DIMESIONE JSON FILES {lj} DIVERSA DA IMG FILES {li}")
    exit()
