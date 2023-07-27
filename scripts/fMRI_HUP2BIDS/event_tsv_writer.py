import pandas as pd
import numpy as np
import nibabel as nib
import json, os

from pathlib import Path

import clean

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def _parse_design_name(design_file_path: str) -> str:
    """
    Parse design file path for task_name of form task-______
    """
    file_name = design_file_path.split("/")[-1] #should be last in path
    task_name = file_name.split("_")[2] #third in bids naming system
    
    #XXX: parsed names may differ from heuristic, update this to switch to consistent names
    name_map = {'task-rhyming': 'task-rhyme', 
                'task-verbgeneration': 'task-verbgen', 
                'task-wordgeneration': 'task-wordgen',}
    if task_name in name_map:
        task_name = name_map[task_name]
    
    return task_name
    
def _read_design(design_file_path: str) -> pd.DataFrame:
    """
    Read design files and return pandas DataFrame containing information
    Refer to .json sidecard for TR to compute duration
    
    design_file_path of form 
    ./bids_temps/design_files/sub-xxx/ses-xxx/func/sub-xxx_ses-xxx_task-xxx_run-01_bold
    """
    design_image = nib.load(design_file_path[:-1] + '.nii.gz')
    design_data = design_image.get_fdata() # type: ignore
    
    #load a meaningful row of image, dimensions: (num_imgs, 120, 1)
    design_row = design_data.squeeze()[:][82]
    first_onset, images, weight = 0, 0, True if design_row[0] else False
    last_value = design_row[0]
    
    #scan row for changes to mark end
    onsets, durations, weights = [], [], []
    for i in design_row:
        if i != last_value:
            onsets.append(first_onset)
            durations.append(images - first_onset)
            weights.append(weight)
            weight = not weight
            first_onset = images
            last_value = i
        images += 1
    onsets.append(first_onset)
    durations.append(images - first_onset)
    weights.append(weight)
    
    #get tr, modify information
    tr = None
    with open(design_file_path[:-1] + '.json', 'r') as file:
        design_info = json.load(file)
        tr = design_info["RepetitionTime"]
    onsets = [tr * i for i in onsets]
    durations = [tr * i for i in durations]
    trial_types = ['stimulus' if i else 'baseline' for i in weights]
    
    #load information into dataframe
    task_info = {
        'onset': onsets,
        'duration': durations,
        'trial_type': trial_types,
    }
    task_dataframe = pd.DataFrame(task_info, 
                        columns = ['onset', 'duration','trial_type'])
    return task_dataframe
    
def _write_tsvs(func_folder_path: str, design_file_paths: str) -> None:
    """
    Read design_file_paths for design files,
    read each design file for task structure,
    write each to corresponding tsv in func_folder_path
    
    func_folder_path: of the form ./bids_data/sub-___/ses-___/func
    design_file_paths: bids_temps/design_files.txt
    """
    func_path_object = Path(func_folder_path).absolute()
    session = str(func_path_object).split("/")[-2]
    subject = str(func_path_object).split("/")[-3]
    
    try:
        with open(design_file_paths, 'r') as design_files:
            
            for design_file_path in design_files:
                
                task_name = _parse_design_name(design_file_path)
                design_dataframe = _read_design(design_file_path)
                #TODO: fix hardcoding of run number
                
                file_name_1 = f'{subject}_{session}_{task_name}_run-01_events.tsv'
                file_path = str(func_path_object) + '/' + file_name_1
                design_dataframe.to_csv(file_path, sep = '\t')
                
                file_name_2 = f'{subject}_{session}_{task_name}_run-02_events.tsv'
                file_path = str(func_path_object) + '/' + file_name_2
                if os.path.isfile(file_path):
                    design_dataframe.to_csv(file_path, sep = '\t', index = False)
    except:
        with open(WORKING_FOLDER_PATH + 'bids_outputs/log.txt', 'a') as file:
            file.write(f'{subject} has no design files\n')
            clean.clean_up('bids_temps/design_files', False)
            
def create_tsv():
    with open(WORKING_FOLDER_PATH + 'path_info.json', 'r') as file:
        path_info = json.load(file)
        _write_tsvs(path_info["func_dir"], WORKING_FOLDER_PATH + 'bids_temps/design_files.txt')