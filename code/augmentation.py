'''
    SCRIPT FOR DATA AUGMENTATION
    This script resize and convert to black and white and brightness each .jpg image in the three folder val, train and test 
    adding given prefixs.
    At the same time it takes all the .txt annotation files and does exactly the same renaming for each file, to
    have correspondence between images and labels.
    This procedure is applied for both val, train and test.
    I added a progress bar to help the user understand how far the conversion has reached.
    
    AFTER:  
    fine_tuning.py to train the newly created dataset
        OR
    TrainYolov8CustomDataset.ipynb on google Colab selecting 'Modifica' --> 'Impostazioni blocco Note' --> 'Acceleratore Hardware' --> T4 GPU --> 'Salva'
    
    The first choice train cNN on your device (VERY VERY SLOW and HEAVY)
    The second one is faster and less computational for the device, but needs stable internet connection!

    author: Alberto Dal Bosco 
    date: 22/11/2023
'''

import cv2
import os
from tqdm import tqdm  # Assicurati di aver installato la libreria tqdm: pip install tqdm
import random
import numpy as np
import shutil



# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM, AND THE PREFIX, w, h
#path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"              #       <---------      MODIFY HERE
path_to_project_folder = "/Users/alberto/Desktop/db" 
prefix_r = "r"
prefix_rbw = "rbw"
prefix_rl = "rl"
delete_original = False
w = 640
h = 640

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
path_to_frame_folder = path_to_videos_folder + "/frame"


def resize_and_convert(input_path, output_path_r, output_path_rbw, output_path_rl, width, height, delete_original=False):
    try:
        # Load the image
        img = cv2.imread(input_path)

        # Resize the image
        resized_img = cv2.resize(img, (width, height))

        # Convert resized image to black and white image
        bw_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

        # Generate a random value for brightness variation
        brightness_factor = random.uniform(0.5, 1.5)

        # Modify the brightness of the image
        augmented_image = cv2.convertScaleAbs(resized_img, alpha=brightness_factor, beta=0)

        # Save the bwr image
        cv2.imwrite(output_path_rbw, bw_img)
        
        # Save the augmented image
        cv2.imwrite(output_path_rl, augmented_image)

        # Delete original image if requested
        if delete_original == False:
            # Save the resized image
            cv2.imwrite(output_path_r, resized_img)
            
        os.remove(input_path)

    except Exception as e:
        print(f"Error during resizing and convertion {input_path}: {str(e)}")



def resize_and_convert_in_folder(folder_path, width, height, delete_original=False, rename=False, prefix_rbw="rbw", prefix_rl="rl"):
    try:
        # Ensure that the folder path ends with '/'
        if not folder_path.endswith('/'):
            folder_path += '/'

        # Get the list of files to process
        file_list = [filename for filename in os.listdir(folder_path) if filename.lower().endswith(".jpg")]

        # Initialize progress bar
        progress_bar = tqdm(total=len(file_list), desc="Processing images")

        # Scan the folder
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".jpg"):
                input_path = os.path.join(folder_path, filename)

                # Generate the name for the resized and converted file
                output_filename_rbw = f"{prefix_rbw}_{filename}" if rename else filename
                output_path_rbw = os.path.join(folder_path, output_filename_rbw)

                # Generate the name for the resized and converted file
                output_filename_rl = f"{prefix_rl}_{filename}" if rename else filename
                output_path_rl = os.path.join(folder_path, output_filename_rl)

                # Generate the name for the resized image
                output_filename_r = f"{prefix_r}_{filename}" if rename else filename
                output_path_r = os.path.join(folder_path, output_filename_r)

                # Resize and convert the image in gray scale and brightness
                resize_and_convert(input_path, output_path_r, output_path_rbw, output_path_rl, width, height, delete_original)

                # Update progress bar
                progress_bar.update(1)
        # Close the progress bar
        progress_bar.close()

    except Exception as e:
        print(f"Error during resizing and conversion of images in the folder {folder_path}: {str(e)}")



# Function to rename text files in a folder
def rename_txt_files(folder_path, delete_original=False, prefix_r="r", prefix_rbw="rbw", prefix_rl="rl"):
    try:
        # Ensure that the folder path ends with '/'
        if not folder_path.endswith('/'):
            folder_path += '/'

        # Get the list of files to process
        file_list = [filename for filename in os.listdir(folder_path) if filename.lower().endswith(".txt")]

        # Initialize progress bar
        progress_bar = tqdm(total=len(file_list), desc="Renaming text files")

        # Scan the folder
        for filename in file_list:
            input_path = os.path.join(folder_path, filename)

            # Generate the new name for the text file
            new_filename_rbw = f"{prefix_rbw}_{filename}"
            new_path_rbw = os.path.join(folder_path, new_filename_rbw)

            # Generate the new name for the text file
            new_filename_rl = f"{prefix_rl}_{filename}"
            new_path_rl = os.path.join(folder_path, new_filename_rl)

            # Generate the new name for the text file
            new_filename_r = f"{prefix_r}_{filename}"
            new_path_r = os.path.join(folder_path, new_filename_r)

            # Copy the text file
            shutil.copy(input_path, new_path_rbw)

            # Copy the text file
            shutil.copy(input_path, new_path_rl)

            # Delete original annotation if requested
            if delete_original == False:
                # Copy the text file
                shutil.copy(input_path, new_path_r)
            
            os.remove(input_path)
            
            # Update progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

    except Exception as e:
        print(f"Error during renaming text files in the folder {folder_path}: {str(e)}")



print("\nTRAIN FOLDER")
resize_and_convert_in_folder(path_to_images_train_folder, w, h, delete_original=delete_original, rename=True, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)
rename_txt_files(path_to_labels_train_folder, delete_original=delete_original, prefix_r = prefix_r, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)

print("\nVAL FOLDER")
resize_and_convert_in_folder(path_to_images_val_folder, w, h, delete_original=delete_original, rename=True, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)
rename_txt_files(path_to_labels_val_folder, delete_original=delete_original, prefix_r = prefix_r, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)


print("\nTEST FOLDER")
resize_and_convert_in_folder(path_to_images_test_folder, w, h, delete_original=delete_original, rename=True, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)
rename_txt_files(path_to_labels_test_folder, delete_original=delete_original, prefix_r = prefix_r, prefix_rbw = prefix_rbw, prefix_rl=prefix_rl)


