'''
    SCRIPT FOR DATA AUGMENTATION
    This script resize and convert to black and white each .jpeg image in the three folder val, train and test 
    adding a given prefix.
    At the same time it takes all the .txt annotation files and does exactly the same renaming for each file, to
    have correspondence between images and labels.
    This procedure is applied for both val, train and test.
    I added a progress bar to help the user understand how far the conversion has reached.
    
    AFTER:  
    fine_tuning.py to train the newly created dataset
    
    author: Alberto Dal Bosco 
    date: 22/11/2023
'''

import cv2
import os
from tqdm import tqdm  # Assicurati di aver installato la libreria tqdm: pip install tqdm



# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM, AND THE PREFIX, w, h
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"              #       <---------      MODIFY HERE
prefix = "rbw"
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


def resize_and_convert_to_bw(input_path, output_path, width, height, delete_original=False, rename=False, prefix="rbw"):
    try:
        # Leggi l'immagine con OpenCV
        img = cv2.imread(input_path)

        # Ridimensiona l'immagine
        resized_img = cv2.resize(img, (width, height))

        # Converti l'immagine in scala di grigi
        bw_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

        # Salva l'immagine ridimensionata e in scala di grigi
        cv2.imwrite(output_path, bw_img)

        # Elimina l'immagine originale se richiesto
        if delete_original:
            os.remove(input_path)

    except Exception as e:
        print(f"Errore durante il ridimensionamento e la conversione in scala di grigi di {input_path}: {str(e)}")



def resize_and_convert_in_folder(folder_path, width, height, delete_original=False, rename=False, prefix="rbw"):
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
                output_filename = f"{prefix}_{filename}" if rename else filename
                output_path = os.path.join(folder_path, output_filename)

                # Resize and convert the image
                resize_and_convert_to_bw(input_path, output_path, width, height, delete_original, rename)
                # Update progress bar
                progress_bar.update(1)
        # Close the progress bar
        progress_bar.close()

    except Exception as e:
        print(f"Error during resizing and black-and-white conversion of images in the folder {folder_path}: {str(e)}")



# Function to rename text files in a folder
def rename_txt_files(folder_path, prefix):
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
            new_filename = f"{prefix}_{filename}"
            new_path = os.path.join(folder_path, new_filename)

            # Rename the text file
            os.rename(input_path, new_path)

            # Update progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

    except Exception as e:
        print(f"Error during renaming text files in the folder {folder_path}: {str(e)}")



print("\nTRAIN FOLDER")
resize_and_convert_in_folder(path_to_images_train_folder, w, h, delete_original=True, rename=True, prefix=prefix)
rename_txt_files(path_to_labels_train_folder, prefix)

print("\nVAL FOLDER")
resize_and_convert_in_folder(path_to_images_val_folder, w, h, delete_original=True, rename=True, prefix=prefix)
rename_txt_files(path_to_labels_val_folder, prefix)

print("\nTEST FOLDER")
resize_and_convert_in_folder(path_to_images_test_folder, w, h, delete_original=True, rename=True, prefix=prefix)
rename_txt_files(path_to_labels_test_folder, prefix)


