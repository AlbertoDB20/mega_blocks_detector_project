# Python program to read
# json file
 
import json
import os
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

# Get all files in the "assigns" folder
files_in_assigns = os.listdir(path_to_assigns_folder)



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
        print("")
except OSError:
   print("ERROR: no assigns folder found")




# function to create .txt annotation file in the form:________img_#num_label.txt_________ 
def create_txt_annotation(path_json, path_txt_folder):
    path_to_txt_annotation_file = path_txt_folder + img + cont_lab + "_label.txt"
    # Apre il file JSON e carica i dati
    with open(path_json, 'r') as file:
        data = json.load(file)

    # Ora puoi accedere ai dati come desideri. Ad esempio, se il file JSON contiene una chiave 'bbox', puoi fare qualcosa del genere:
    if key in data and subkey in data[key]:
        values = data[key][subkey]
        # Ora puoi lavorare con i dati della bounding box come richiesto nel tuo script 3d_bbox_pixel_space.
        with open(path_to_txt_annotation_file, 'w') as annotation_file:
            annotation_file.write(str(values))                                      # TODO: call here a function to create YOLO annotation
    else:
        print("La sottochiave {subkey} non è presente nel file JSON.")


def save_img(img_file_path, path_to_images):
    # Extract the file name and extension from the original image
    file_name, extension = os.path.splitext(os.path.basename(img_file_path))                # in our case, file_name is view=#num

    # Modify the file name as desired (e.g., add a prefix)
    new_file_name = img + cont_img + extension

    # Create the new full path for the image in the destination folder
    new_image_path = os.path.join(path_to_images, new_file_name)

    # Copy the image to the new location with the new name
    shutil.copyfile(img_file_path, new_image_path)





# Filter only files with the ".json" extension
for file_name in files_in_assigns:
    if file_name.endswith(".json"):
        json_files.append(file_name)
    if file_name.startswith("view=") and file_name.endswith(".jpeg") and "_vertices" not in file_name and "_depth" not in file_name and "_depth_plane" not in file_name and "_bbox" not in file_name:
        img_files.append(file_name)

# Call the create_txt_annotation function for each JSON file
for json_file in json_files:
    # Construct the full path for the JSON file
    json_file_path = os.path.join(path_to_assigns_folder, json_file)
    # Call the create_txt_annotation function with the file path as a parameter
    create_txt_annotation(json_file_path, path_to_txt_labels)
    

# Call the save_img function for each images found
for img_file in img_files:
    # Construct the full path for the JSON file
    img_file_path = os.path.join(path_to_assigns_folder, img_file)
    # Call the save_img function with the file path as a parameter
    save_img(img_file_path, path_to_images)
