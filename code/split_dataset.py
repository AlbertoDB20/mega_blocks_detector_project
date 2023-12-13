'''
    
    PYTHON SCRIPT FOR SPLITTING DATASETS.
    This python script moves the .jpeg images into the three sub-folder train, val, test in a given percentage
   
    
    BEFORE COMPILING:
    For the import library, are mandatory this commands:   (N.B.: macOS command line)
        pip install moviepy

    AFTER:  
    augmentation.py to augment train and validation dataset
    
    
    author: Alberto Dal Bosco 
    date: 13/12/2023

'''


import os
from moviepy.editor import *
from tqdm import tqdm
import random
import shutil

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/autovelox_detector_project"              #       <---------      MODIFY HERE

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



# Necessary variable
contatore = 0
currentFrame = 0
percentage_train = 0.7
percentage_val = 0.15
percentage_test = 0.15



# function to split images into the three subdirectory train, val and test.
def split_images(images_directory, l_dir, train_directory, tl_dir, validation_directory, vl_dir, test_directory, testl_dir, x, y, z):
    # I create the folder train, validation, testing for images
    try: 
        if not os.path.exists(train_directory):
            os.makedirs(train_directory)
    except OSError:
        print("ERROR in creating directory {train_directory}")

    try: 
        if not os.path.exists(validation_directory):
            os.makedirs(validation_directory)
    except OSError:
        print("ERROR in creating directory {validation_directory}")

    try: 
        if not os.path.exists(test_directory):
            os.makedirs(test_directory)
    except OSError:
        print("ERROR in creating directory {test_directory}")

    # I create the folder train, validation, testing for labels
    try: 
        if not os.path.exists(tl_dir):
            os.makedirs(tl_dir)
    except OSError:
        print("ERROR in creating directory {tl_dir}")

    try: 
        if not os.path.exists(vl_dir):
            os.makedirs(vl_dir)
    except OSError:
        print("ERROR in creating directory {vl_dir}")

    try: 
        if not os.path.exists(testl_dir):
            os.makedirs(testl_dir)
    except OSError:
        print("ERROR in creating directory {testl_dir}")


    
    #Splitting of three sub-folder
    split = (x, y, z)
    
    # List of files in the "images" folder
    image_files = [f for f in os.listdir(images_directory) if f.endswith('.jpeg')]
    label_files = [f for f in os.listdir(l_dir) if f.endswith('.txt')]

    image_files.sort()
    label_files.sort()

    # Calculate the number of images for each set
    total_images = len(image_files)
    total_labels = len(label_files)

    if(total_images != total_labels):
        print("ERROR: DIFFERENT NUMBER OF IMAGES AND LABELS")
        exit()

    num_train = int(split[0] * total_images)
    num_validation = int(split[1] * total_images)


    # Generate random indices to select images
    random_indices = random.sample(range(total_images), total_images)

    # Initialize tqdm for progress bar
    progress_bar_images = tqdm(total=total_images, desc='   Moving Images', unit='image')
    progress_bar_labels = tqdm(total=total_labels, desc='   Moving Labels', unit='label')
 
    # Move images to the appropriate sets
    for i, index in enumerate(random_indices):
        source_image_path = os.path.join(images_directory, image_files[index])
        source_label_path = os.path.join(l_dir, label_files[index])
        if i < num_train:
            destination_image_path = os.path.join(train_directory, image_files[index])
            destination_label_path = os.path.join(tl_dir, label_files[index])
        elif i < num_train + num_validation:
            destination_image_path = os.path.join(validation_directory, image_files[index])
            destination_label_path = os.path.join(vl_dir, label_files[index])
        else:
            destination_image_path = os.path.join(test_directory, image_files[index])
            destination_label_path = os.path.join(testl_dir, label_files[index])

        # Move the image
        shutil.move(source_image_path, destination_image_path)      # shutil.copy() to copy
        shutil.move(source_label_path, destination_label_path)

        # Update the progress bar
        progress_bar_images.update(1)
        progress_bar_labels.update(1)

    # Close the progress bar
    progress_bar_images.close()
    progress_bar_labels.close()

    print(f"\n\nImages successfully moved to:\n- Train: {num_train} images\n- Validation: {num_validation} images\n- Test: {total_images - num_train - num_validation} images")
    print(f"\n\nLabels successfully moved to:\n- Train: {num_train} labels\n- Validation: {num_validation} labels\n- Test: {total_images - num_train - num_validation} labels")


print("\n\n\nSPLIT IMAGES INTO SUB FOLDER\n\n")
split_images(path_to_images_folder, path_to_labels_folder, path_to_images_train_folder, path_to_labels_train_folder , path_to_images_val_folder, path_to_labels_val_folder , path_to_images_test_folder , path_to_labels_test_folder , percentage_train, percentage_val, percentage_test)
