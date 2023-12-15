'''
    
    PYTHON SCRIPT FOR CREATING DATASETS.
    This python script make three important operation:
    1) takes as input the folder containing all the .MOV videos and convert it in .mp4 format in a specific folder
    2) for all the .mp4 video in the MP4_FOLDER, the script save in image folder the associated frames in .jpg format.
        N.B.: it automatically creates image folder and MP4_video folder, but the .MOV one is necessary to the correct working flow of the script.
   
    
    BEFORE COMPILING:
    For the import library, are mandatory this commands:   (N.B.: macOS command line)
        pip install moviepy
        pip install cv2

    Set to True or False three boolean variable according to the goal of the project to allow one or more of the 
    aforementioned operations.

    AFTER:  
    augmentation.py to augment train and validation dataset
    
    
    author: Alberto Dal Bosco 
    date: 22/11/2023

'''

import os
from moviepy.editor import *
from tqdm import tqdm
import cv2
import subprocess

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
path_to_frame_folder = path_to_videos_folder + "/frame"



# Put True or False in this flags, according to your code
DO_YOU_HAVE_MOV_VIDEO_TO_CONVERT = True
DO_YOU_HAVE_MP4_VIDEO_TO_FRAME = True
DO_YOU_WANT_TO_EXTRACT_SQUARE_FRAME = True
split = 50                              # if a video has 1000 frame, it take frame 0 and multiple of split


# Bash command to execute
bash_command = "open " + str(path_to_videos_folder) + "/ANNOTATION_PROCEDURE.md"



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
    global split
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
                if i%split==0:
                    frame_path = f"{output_folder}/{get_filename_without_extension(video_name)}__frame_{count}.jpeg"
                    cv2.imwrite(frame_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # Imposta la qualità dell'immagine a 90 (valore tipico)

                # Leggi il prossimo frame
                success, frame = video.read()
                count += 1
        # Chiudi il video
        video.release()



def extract_central_image(input_path, output_path):
    # Load the input image
    image = cv2.imread(input_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Unable to load the image: {input_path}")
        return

    # Get the dimensions of the input image
    height, width = image.shape[:2]

    new_size = min(height, width)

    # Calculate the coordinates of the Region of Interest (ROI)
    start_x = width // 2 - new_size // 2
    start_y = height // 2 - new_size // 2
    end_x = start_x + new_size
    end_y = start_y + new_size

    # Extract the central image (ROI)
    extracted_image = image[start_y:end_y, start_x:end_x]

    # Save the extracted image
    cv2.imwrite(output_path, extracted_image)



def process_images_in_folder(folder_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get the list of JPEG files in the input folder
    image_files = [filename for filename in os.listdir(folder_path) if filename.lower().endswith('.jpeg')]

    # Initialize tqdm to create a progress bar
    progress_bar = tqdm(total=len(image_files), desc=" Extracting square frame: ")


    # Loop through all files in the input folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpeg'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Call the function to extract the central image
            extract_central_image(input_path, output_path)
            
            # Update the progress bar
            progress_bar.update(1)
    
    # Loop through all files in the input folder to delete previous frame
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpeg'):
            try:
                file_path = os.path.join(folder_path, filename)
                # Remove the file given the directory
                os.remove(file_path)
            except FileNotFoundError:
                print(f"Error: file {file_path} was not found.")
            except Exception as e:
                print(f"Error while deleting the file {file_path}: {e}")
    
    # Close the progress bar
    progress_bar.close()



########################################################################    MAIN    ########################################################################################################


def main():
    # I first convert all the .MOV video in .mp4 format 
    if DO_YOU_HAVE_MOV_VIDEO_TO_CONVERT:
        convert_mov_to_mp4(path_to_videos_MOV_folder, path_to_videos_MP4_folder)

    if DO_YOU_HAVE_MP4_VIDEO_TO_FRAME:
        # then I take all the .mp4 video and I frame it, saving .jpg frames in image folder 
        for root, dirs, files in os.walk(path_to_videos_MP4_folder):
            for vid in files:
                video_path = path_to_videos_MP4_folder + "/" + vid
                frammenta_video(video_path, path_to_videos_folder, vid)
    
    if DO_YOU_WANT_TO_EXTRACT_SQUARE_FRAME:
        # Call the function to process all images in the input folder
        process_images_in_folder(path_to_videos_folder, path_to_frame_folder)

    #print("\n\n\n\t\t\t\tNOW YOU HAVE TO ANNOTATE THE SQUARED IMAGES ALREADY FRAMED.\nGo to https://app.roboflow.com, \n--> Sign in\n--> Create new project (Object Detection) and create \n--> Add Classes \n--> Upload Images, in our case are in frame folder (click Save and Continue) \n--> Assign images to group component, if existent (click Assign button) \n--> Annotate Images (click Start Annotating) \n\t\tHere you have to annotate each image with the Bounding Box Tool selecting for each BB the correct class. \n\t\tRepeat this procedure for all the images non annotated. \n\t\tWhen finished, click on the 'back arrow' and click Add # images to Datasets selecting correct proportionality for Image Distribution \n\t\tIn conclusion, click Add Images \n--> Click on Projects in the roboflow main header and select current project \n--> Do not select any Preprocessing transformation (click Continue) \n--> Do not select any Augmentation for your image (click Continue) \n--> CLICK CREATE to create first version of your dataset \n--> Export Dataset selecting YOLOv8 Format and -download zip to computer- option (click Continue) \nGo to download folder and copy/move train, val, test folder of images and labels in corresponding train, val, test folder of your project (test does not have labels obviusly). \nNow it is time to augment this images and those already present in that folder (GO TO augmentation.py script) \n\t\t\t____________________     YOU CAN CLOSE THIS FILE!!        ____________________  \n\n\n")

    # Execute the Bash command
    try:
        output = subprocess.check_output(bash_command, shell=True, text=True)
        print("Command output:\n", output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

########################_____________THIS WILL BE EXECUTED______________##################################

main()
