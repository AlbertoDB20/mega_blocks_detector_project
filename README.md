WAY TO CREATE DATASETS:

N.B.: you have to adapt bash 

1) Modify in create_all_project_folder.py the path_to_project_folder, according to your system, then compile this scripts.

            cd path_to_python_script

2) Save all your .MOV video into the path_to_videos_MOV_folder renaming videos as yuo want. I really suggest to rename it such as "img001.MOV" even if they are not img. 

            mv ....     or    cp .....
3) compile create_datasets.py. Now you will have all the frame of all the video well organized into the three sub-directory train, val, test.

            python3 path_to_python_script + create_dataset.py 
            
4) now it is the moment to take all the .jpg images in train images folder and annotate it using, for example, CVAT online annotator tool. Save the annotation in the correct format of datasets into the train labels folder.


5) re-do previous passage for validation.



TODO: 

--> script python that takes all the train images and its label and it modifies if, such as:
    - black and white 
    - resize 

DONE!