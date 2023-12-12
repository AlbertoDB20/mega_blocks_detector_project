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

from PIL import Image
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



def resize_and_convert_to_bw(input_path, output_path, width, height, delete_original=False, rename=False, prefix="rbw"):
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize((width, height))

            # Convert the image to black and white
            bw_img = resized_img.convert("L")

            # Generate the output filename based on the original or a new name
            if rename:
                output_filename = f"{prefix}_{os.path.basename(input_path)}"
            else:
                output_filename = os.path.basename(input_path)

            output_path = os.path.join(os.path.dirname(input_path), output_filename)

            # Save the resized and black-and-white image
            bw_img.save(output_path)

        # Delete the original image if requested
        if delete_original:
            os.remove(input_path)

    except Exception as e:
        print(f"Error during resizing and black-and-white conversion of {input_path}: {str(e)}")


def resize_and_convert_in_folder(folder_path, width, height, delete_original=False, rename=False, prefix="rbw"):
    try:
        # Ensure that the folder path ends with '/'
        if not folder_path.endswith('/'):
            folder_path += '/'

        # Get the list of files to process
        file_list = [filename for filename in os.listdir(folder_path) if filename.lower().endswith(".jpeg")]

        # Initialize progress bar
        progress_bar = tqdm(total=len(file_list), desc="Processing images")

        # Scan the folder
        for filename in file_list:
            input_path = os.path.join(folder_path, filename)

            # Generate the name for the resized and converted file
            output_filename = f"{prefix}_{filename}" if rename else filename
            output_path = os.path.join(folder_path, output_filename)

            # Resize and convert the image
            resize_and_convert_to_bw(input_path, output_path, width, height, delete_original, rename, prefix)

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


#TODO: capire per qualche cavolo di ragione mi da 
#               Corrupt JPEG data: premature end of data segment
#       quando faccio fine_tuning.py