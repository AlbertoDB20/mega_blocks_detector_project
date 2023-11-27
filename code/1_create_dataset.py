'''
    FUNZIONA!!
    
        PYTHON SCRIPT FOR CREATING DATASETS.
    This python script make two important operation:
    1) takes as input the folder containing all the .MOV videos and convert it in .mp4 format in a specific folder
    2) for all the .mp4 video in the MP4_FOLDER, the script save in image folder the associated frames in .jpg format.
        N.B.: it automatically creates image folder and MP4_video folder, but the .MOV one is necessary to the correct working flow of the script.
    3) it moves the .jpg images into the three sub-folder train, val, test in a given percentage
   
    For the import library, are mandatory this commands:   (N.B.: macOS command line)
    
    pip install moviepy
    pip install cv2
    

    author: alberto dal bosco 
    date: 22/11/2023
'''

import os
from moviepy.editor import *
from tqdm import tqdm
import cv2
import sys
import random
import shutil

# CHANGE ONLY THIS FOLDER, ACCORDING TO THE STRUCTURE OF YOUR FILESYSTEM
path_to_project_folder = "/Users/alberto/ROBOTICS/test_scrips"

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
percentage_train = 0.6
percentage_val = 0.2
percentage_test = 0.2



# I create the folder
try: 
   if not os.path.exists(path_to_images_folder):
      os.makedirs(path_to_images_folder)
except OSError:
   print("ERROR in creating directory for image")

try: 
   if not os.path.exists(path_to_videos_MOV_folder):
      os.makedirs(path_to_videos_MOV_folder)
except OSError:
   print("ERROR in creating directory for MOV videos")

try: 
   if not os.path.exists(path_to_videos_MP4_folder):
      os.makedirs(path_to_videos_MP4_folder)
except OSError:
   print("ERROR in creating directory for MP4 videos")




# function to create progress bar (or use tqdm)    --> for i in progressbar(range(15), "Computing: ", 40): time.sleep(0.1)
def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()
        file.write("\n")

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
        file.write("\n")
    file.flush()




# function to convert .MOV video to .mp4 format
def convert_mov_to_mp4(input_folder, output_folder):
    print("\n\n\nCONVERTING .MOV VIDEO TO .MP4\n\n")
    try:
        # Get a list of all .mov files in the input folder
        mov_files = [filename for filename in os.listdir(input_folder) if filename.endswith(".MOV")]
        # Loop through all .mov files and show estimated progress with a progress bar
        for filename in tqdm(mov_files, desc='    Convertion: ', unit='video'):
            if not filename.endswith('.MOV'):
                raise ValueError("Input file must have .mov extension")
            # Get the full file path of the input .mov file
            input_file_path = os.path.join(input_folder, filename)
            
            # Load the .mov file
            video = VideoFileClip(input_file_path)
            
            # Get the duration of the video in seconds
            duration = video.duration
            
            # Estimate the total number of frames to be written based on duration and frame rate
            total_frames = int(duration * video.fps)
            
            # Construct the output file name with .mp4 extension
            output_filename = os.path.splitext(filename)[0] + ".mp4"
            
            # Construct the output file path
            output_file_path = os.path.join(output_folder, output_filename)
            
            # Convert and save the video to .mp4 in the output folder
            video.write_videofile(output_file_path, codec='libx264', fps=video.fps, audio = False)
            
            # Update the progress manually based on the progress of video writing
            progress = 0
            with tqdm(total=total_frames, desc=f'{filename}', unit='frame') as pbar:
                while progress < total_frames:
                    # Update progress based on the number of frames written
                    progress = video.reader.nframes
                    pbar.update(progress - pbar.n)
        return True
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return False
    



# function to get filename without extension
def get_filename_without_extension(file_name):
    name, extension = os.path.splitext(file_name)
    return name




# Function to fragment a .mp4 video to .jpg images
def frammenta_video(video_path, output_folder, video_name):
    # Apri il video
    if video_name.endswith('.mp4'):
        print("\n\n\nFRAGMENTATION of", video_name, "\n")

        video = cv2.VideoCapture(video_path)
        frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Verifica se il video è stato aperto correttamente
        if not video.isOpened():
            print(f"\n\tErrore nell'apertura del video: {video_path}")
            return

        # Leggi i frame dal video
        success, frame = video.read()
        count = 0
        # Leggi e frammenta i frame fino a quando ci sono frame disponibili
        if success:
            for i in tqdm(range(frame_number), desc = "     Frame: ", unit = "frame"):
                # Salva il frame come immagine JPG
                frame_path = f"{output_folder}/{get_filename_without_extension(video_name)}__frame_{count}.jpg"
                cv2.imwrite(frame_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # Imposta la qualità dell'immagine a 90 (valore tipico)

                # Leggi il prossimo frame
                success, frame = video.read()
                count += 1
        # Chiudi il video
        video.release()
   



# function to split images into the three subdirectory train, val and test.
def split_images(images_directory, train_directory, validation_directory, test_directory, x, y, z):
    # I create the folder train, validation, testing
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
    
    #Splitting of three sub-folder
    split = (x, y, z)
    
    # List of files in the "images" folder
    image_files = [f for f in os.listdir(images_directory) if f.endswith('.jpg')]

    # Calculate the number of images for each set
    total_images = len(image_files)
    num_train = int(split[0] * total_images)
    num_validation = int(split[1] * total_images)

    # Generate random indices to select images
    random_indices = random.sample(range(total_images), total_images)

    # Initialize tqdm for progress bar
    progress_bar = tqdm(total=total_images, desc='   Moving Images', unit='image')

    # Move images to the appropriate sets
    for i, index in enumerate(random_indices):
        source_path = os.path.join(images_directory, image_files[index])
        if i < num_train:
            destination_path = os.path.join(train_directory, image_files[index])
        elif i < num_train + num_validation:
            destination_path = os.path.join(validation_directory, image_files[index])
        else:
            destination_path = os.path.join(test_directory, image_files[index])

        # Move the image
        shutil.move(source_path, destination_path)      # shutil.copy() to copy

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    print(f"\n\nImages successfully moved to:\n- Train: {num_train} images\n- Validation: {num_validation} images\n- Test: {total_images - num_train - num_validation} images")





########################################################################    MAIN    ########################################################################################################


def main():
    # I first convert all the .MOV video in .mp4 format 
    convert_mov_to_mp4(path_to_videos_MOV_folder, path_to_videos_MP4_folder)


    # then I take all the .mp4 video and I frame it, saving .jpg frames in image folder 
    for root, dirs, files in os.walk(path_to_videos_MP4_folder):
        for vid in files:
            video_path = path_to_videos_MP4_folder + "/" + vid
            frammenta_video(video_path, path_to_images_folder, vid)

    # Now it is time to create the datasets, now I have to arrange the image in images into the three folders
    print("\n\n\nDIVIDE IMAGES INTO SUB FOLDER\n\n")
    split_images(path_to_images_folder, path_to_images_train_folder, path_to_images_val_folder, path_to_images_test_folder, percentage_train, percentage_val, percentage_test)
    
    print("\n\n\nFINISHED\n\n")



########################_____________THIS WILL BE EXECUTED______________##################################

main()
