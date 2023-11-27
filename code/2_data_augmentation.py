'''
        SCRIPT FOR DATA AUGMENTATION

        pip install albumentations
        pip install Pillow

        PRINCIPLE:
        1) verify existence of path_to_images_train_folder, path_to_images_val_folder, path_to_images_test_folder
        2) verify existence of path_to_labels_train_folder, path_to_labels_val_folder, path_to_labels_test_folder
        Now I consider only one of the previous three couple of folder  (easly path_image & path_label)
        3) I take one image from the path_image and its correspondent label file from path_label
        4) 
        



'''
import albumentations as A
from albumentations import Resize
from PIL import Image
import os
import numpy as np
import shutil


def load_annotations(annotation_directory, image_file):
    annotation_file = os.path.join(annotation_directory, f"{os.path.splitext(image_file)[0]}.txt")

    annotations = []

    with open(annotation_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            values = line.strip().split()
            if len(values) == 5:
                class_index = int(values[0])
                x_center, y_center, width, height = map(float, values[1:])
                annotations.append((class_index, x_center, y_center, width, height))

    return annotations

def save_annotations_yolo_1_1(annotation_path, annotations):
    with open(annotation_path, 'w') as f:
        for annotation in annotations:
            class_index, x_center, y_center, width, height = annotation

            # Convert normalized coordinates to image-specific coordinates
            x_center *= width
            y_center *= height
            width *= width
            height *= height

            line = f"{class_index} {x_center} {y_center} {width} {height}\n"
            f.write(line)


def convert_to_black_and_white_albumentations(input_image, output_folder):
    # Define the augmentation pipeline
    transform = A.Compose([
        A.ToGray(p=1.0),
    ])
    
    # Load the image
    try:
        image = Image.open(input_image)
    except Exception as e:
        print(f"Error opening the image: {e}")
        return
    
    # Convert the image to a NumPy array
    image_array = np.array(image)
    
    # Apply the augmentation
    augmented = transform(image=image_array)
    
    # Convert the augmented image array back to a PIL image
    augmented_image = Image.fromarray(augmented['image'])

    # Extract the file name and create the path for the output image
    file_name = os.path.basename(input_image)
    output_path = os.path.join(output_folder, f"bw_{file_name}")
    
    # Save the augmented image to the output folder
    try:
        augmented_image.save(output_path)
        print(f"Image converted successfully. Saved to: {output_path}")
    except Exception as e:
        print(f"Error saving the image: {e}")



def resize_image_albumentations(input_image, output_folder, resize_value):
   # Load the image
    try:
        image = Image.open(input_image)
    except Exception as e:
        print(f"Error opening the image: {e}")
        return
    
    final_height = int(resize_value * image.height)
    final_width = int(resize_value * image.width)

    # Definisci la trasformazione di resize
    transform = Resize(
        final_height, 
        final_width
        )

    # Applica la trasformazione
    augmented = transform(image=np.array(image))

    # Ottieni l'immagine ridimensionata
    resized_image = Image.fromarray(augmented['image'])

    # Crea la cartella se non esiste già
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the file name and create the path for the output image
    file_name = os.path.basename(input_image)
    output_path = os.path.join(output_folder, f"rz_{file_name}")

    # Save the augmented image to the output folder
    try:
        resized_image.save(output_path)
        print(f"Image converted successfully. Saved to: {output_path}")
    except Exception as e:
        print(f"Error saving the image: {e}")
    


# function to get filename without extension
def get_filename_without_extension(file_name):
    name, extension = os.path.splitext(file_name)
    return name



def copy_file_with_prefix(input_file, output_folder, prefix):               # prefix example: bw_ or rz_
    # Extract the file name and path
    file_name = os.path.basename(input_file)
    
    # Add the "bw_" prefix to the file name
    new_file_name = f"{prefix}{file_name}"
    
    # Create the full path for the output file
    output_path = os.path.join(output_folder, new_file_name)
    
    try:
        # Copy the file to the new location
        shutil.copy2(input_file, output_path)
        print(f"File copied successfully. Saved to: {output_path}")
    except Exception as e:
        print(f"Error copying the file: {e}")



def augment_images_custom(input_image_directory, output_image_directory, input_annotation_directory, output_annotation_directory, reduce=0.5):
    if not os.path.exists(output_image_directory):
        os.makedirs(output_image_directory)

    if not os.path.exists(output_annotation_directory):
        os.makedirs(output_annotation_directory)

    image_files = [f for f in os.listdir(input_image_directory) if f.lower().endswith('.jpg')]          # here i take all the image_files with the .jpg extension

    for image_file in image_files:
        input_image_path = os.path.join(input_image_directory, image_file)              # path image
        
        convert_to_black_and_white_albumentations(input_image_path, output_image_directory)     # convert image in bw
        resize_image_albumentations(input_image_path, output_image_directory, reduce)
        
        label_file_name = get_filename_without_extension(image_file) + ".txt"               # example: I obtain img_0.txt 
        input_file = os.path.join(input_annotation_directory, label_file_name)

        copy_file_with_prefix(input_file, output_annotation_directory, "bw_")
        copy_file_with_prefix(input_file, output_annotation_directory, "rz_")
    print("Custom data augmentation with annotations using Albumentations completed.")



# Example usage with 70% reduction in dimensions
input_image_directory = "/Users/alberto/ROBOTICS/test_scrips/data/images/train"
output_image_directory = "/Users/alberto/ROBOTICS/test_scrips/data/images/aug_train"
input_annotation_directory = "/Users/alberto/ROBOTICS/test_scrips/data/labels/train"
output_annotation_directory = "/Users/alberto/ROBOTICS/test_scrips/data/labels/aug_train"
augment_images_custom(input_image_directory, output_image_directory, input_annotation_directory, output_annotation_directory, reduce=0.6)

