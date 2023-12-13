# Python program to read
# json file


'''
    SEBE to YOLO script
    This script takes in input Sebe dataset saved in assigns folder and:
        1) move and rename each images in data/images folder
        2) read JSON file for each images, elaborate it computing YOLO annotations and save it in renamed .txt 
           extended file in data/labels folder

    LABEL STRUCTURE: 
    Labels for this format should be exported to YOLO format with one *.txt file per image. 
    If there are no objects in an image, no *.txt file is required. 
    The *.txt file should be formatted with one row per object in class x_center y_center width height format. 
    Box coordinates must be in normalized xywh format (from 0 to 1). 
    If your boxes are in pixels, you should divide x_center and width by image width, and y_center and height by image height. 
    Class numbers should be zero-indexed (start with 0).

    AFTER: 
    dataset_video_&_split.py to randomic split images and labels (set to True SPLIT flag) into three subfolder.

    author: Alberto Dal Bosco 
    date: 2/12/2023

'''
 
import json
import os
import shutil
from tqdm import tqdm


# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"              #       <---------      MODIFY HERE


# path for subfolder: DO NOT MODIFY THIS!
path_to_assigns_folder = path_to_project_folder + "/assigns"
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

# useful string
img = "img_"
subkey1 = 'vertices'
subkey2 = 'bbox'
subkey3 = '3d_bbox'
subkey4 = '3d_bbox_pixel_space'
subkey5 = 'bbox_connections'
subkey6 = 'camera_coordinates'
subkey7 = 'camera_matrix_world_to_translation'
subkey8 = 'camera_rotation_euler'
subkey9 = 'y'
subkey10 = 'obj_rotation_matrix'
subkey11 = 'obj_translation_matrix'

# ID of megablocks
id0 = "X1-Y1-Z2"
id1 = 'X1-Y2-Z1'
id2 = 'X1-Y2-Z2'
id3 = 'X1-Y2-Z2-CHAMFER'
id4 = 'X1-Y2-Z2-TWINFILLET'
id5 = 'X1-Y3-Z2'
id6 = 'X1-Y3-Z2-FILLET'
id7 = 'X1-Y4-Z1'
id8 = 'X1-Y4-Z2'
id9 = 'X2-Y2-Z2'
id10 = 'X2-Y2-Z2-FILLET'

# counter for images and labels files
cont_img = 0
cont_lab = 0

# List to store JSON and images files 
json_files = []
img_files = []

# Size of image
height = 1024
width = 1024


# I create/check the folder
try: 
   if not os.path.exists(path_to_images_folder):
      os.makedirs(path_to_images_folder)
except OSError:
   print("ERROR in creating directory for image")

try: 
   if not os.path.exists(path_to_labels_folder):
      os.makedirs(path_to_labels_folder)
except OSError:
   print("ERROR in creating directory for txt labels")

try: 
   if not os.path.exists(path_to_assigns_folder):
        print("FOLDER READY")
except OSError:
   print("ERROR: no assigns folder found")



def convert_id_to_num(id):
    if id == id0:
        return 0
    elif id == id1:
        return 1
    elif id == id2:
        return 2
    elif id == id3:
        return 3
    elif id == id4:
        return 4
    elif id == id5:
        return 5
    elif id == id6:
        return 6
    elif id == id7:
        return 7
    elif id == id8:
        return 8
    elif id == id9:
        return 9
    elif id == id10:
        return 10
    else: 
        print("ERROR: no matching of id")
        exit()



def remove_numbers(input_string):
    """
    Remove numbers from the input string.

    Parameters:
    - input_string (str): The input string.

    Returns:
    - str: The string without numbers.
    """
    return ''.join(char for char in input_string if not char.isdigit())



def sebe_to_yolo(ulc, drc, w, h):                
    #x_ulc, y_ulc, x_drc, y_drc, x_center_normalized, y_center_normalized, h_bb_normalized, w_bb_normalized = 0
    x_ulc = ulc[0]
    y_ulc = ulc[1]
    x_drc = drc[0]
    y_drc = drc[1]
    w_bb_normalized = (x_drc - x_ulc)/w
    h_bb_normalized = (y_drc - y_ulc)/h
    x_center_normalized = x_ulc/w + w_bb_normalized/2
    if x_center_normalized < 0.0:
        x_center_normalized = 0.0
    elif x_center_normalized > 1.0:
        x_center_normalized = 1.0
    y_center_normalized = y_ulc/h + h_bb_normalized/2
    if y_center_normalized < 0.0:
        y_center_normalized = 0.0
    elif y_center_normalized > 1.0:
        y_center_normalized = 1.0
    return x_center_normalized, y_center_normalized, w_bb_normalized, h_bb_normalized



def find_extreme_coordinates(lista_coordinate):
    if not lista_coordinate:
        return None, None

    # Initialize the extreme coordinates with the first point of the list
    x_min, y_min = lista_coordinate[0]
    x_max, y_max = lista_coordinate[0]

    # Iterate through the remanent coordinates to find the min and max value
    for x, y in lista_coordinate:
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    # Return extreme coordinates
    punto_alto_sinistra = [x_min, y_min]
    punto_basso_destra = [x_max, y_max]
    
    return punto_alto_sinistra, punto_basso_destra



# function to create .txt annotation file in the form:________img_#num_label.txt_________ 
def create_txt_annotation(path_json, path_txt_folder):
    global cont_lab
    new_file_name = img + str(cont_lab) + ".txt"                # img_#num_label.txt

    # Create the new full path for the image in the destination folder
    new_label_path = os.path.join(path_txt_folder, new_file_name)

    # Apre il file JSON e carica i dati
    with open(path_json, 'r') as file:
        data = json.load(file)

    with open(new_label_path, 'w') as annotation_file:
        for key in data:
            vertices = data[key][subkey1]
            bbox = data[key][subkey2]
            bbox_3d = data[key][subkey3]
            bbox_3d_pixel_space = data[key][subkey4]
            bbox_connections = data[key][subkey5]
            camera_coordinates = data[key][subkey6]
            camera_matrix_world_to_translation = data[key][subkey7]
            camera_rotation_euler = data[key][subkey8]
            y = data[key][subkey9]
            obj_rotation_matrix = data[key][subkey10]
            obj_translation_matrix = data[key][subkey11]
            
            id_num = convert_id_to_num(y)
            ulc, drc = find_extreme_coordinates(bbox_3d_pixel_space)            # up left corner and down right corner
            xc, yc, w, h = sebe_to_yolo(ulc, drc, width, height)                # x_center, y_center, width and height of BB

            annotation_file.write(str(id_num) + " " + str(xc) + " " + str(yc) + " " + str(w) + " " + str(h) + "\n")
    cont_lab = cont_lab + 1 




def save_img(img_file_path, path_to_images):
    global cont_img
    # Modify the file name as desired (e.g., add a prefix)
    new_file_name = img + str(cont_img) + '.jpeg'                   # img_#num.jpeg

    # Create the new full path for the image in the destination folder
    new_image_path = os.path.join(path_to_images, new_file_name)

    # Copy the image to the new location with the new name
    shutil.copyfile(img_file_path, new_image_path)
    cont_img = cont_img + 1



############################################################################################################################################################################################################################


pbar = tqdm(os.listdir(path_to_assigns_folder))

# Filter only files with the ".json" extension
for folder_name in pbar:
    if "assign" in folder_name:
        folder_path = os.path.join(path_to_assigns_folder, folder_name)
        for scene_name in os.listdir(folder_path):
            if "scene" in scene_name:                           
                scene_path = os.path.join(folder_path, scene_name)
                json_path_list = []
                img_path_list = []
                for file_name in os.listdir(scene_path):
                    file_path = os.path.join(scene_path, file_name)
                    if file_name.endswith(".json"):
                        json_path_list.append(file_path)
                    if file_name.startswith("view=") and file_name.endswith(".jpeg") and "_vertices" not in file_name and "_depth" not in file_name and "_depth_plane" not in file_name and "_bbox" not in file_name:
                        img_path_list.append(file_path)
                json_path_list.sort()
                img_path_list.sort()
                if(len(json_path_list) != len(img_path_list)):
                    print("ERROR: DO NOT FIND CORRESPONDENT IMAGE FOR AN ANNOTATION")
                    exit()
                for jpath in json_path_list:
                    create_txt_annotation(jpath, path_to_labels_folder)
                for ipath in img_path_list:
                    save_img(ipath, path_to_images_folder)

#print("FIRST 10 ELEMENT (debug):", json_files[:10])


lj = len(json_files)
li = len(img_files)
if (lj != li):
    print("ERRORE: DIMESIONE JSON FILES {lj} DIVERSA DA IMG FILES {li}")
    exit()


#TODO: cambiare nome progetto
#TODO: rendere collabolatori Posky, Fede e Alex
#TODO: guardare fine-tuning di Elia, per capire cosa posso fare di meglio

# kikalore2002@gmail.com
# 

