import json, os
from typing import List
import pandas as pd

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def _parse_json_name(event_json_filename: str):
    task_name = event_json_filename.split('_')[0].split('-')[1]
    return task_name

def _parse_task_name(event_tsv_filename: str):
    task_name = event_tsv_filename.split('_')[2].split('-')[1]
    return task_name

def _get_metadata(subject_num: str, task_name: str):
    tr, image_num = None, None
    func_path = WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/func/'
    filename = f'sub-{subject_num}_ses-001_task-{task_name}_run-01_bold.json'
    with open(func_path + filename, 'r') as file:
        metadata = json.load(file)
        tr = metadata['RepetitionTime']
        image_num = metadata['dcmmeta_shape'][3]
    return tr, image_num

def _load_taskmap():
    task_map = {}
    design_path = WORKING_FOLDER_PATH + f'bids_temps/design_files/'
    for filename in [i for i in os.listdir(design_path) if i[-5:] == '.json']:
        with open(design_path + filename, 'r') as json_file:
            details = json.load(json_file)
            task_name = _parse_json_name(filename)
            task_map[(task_name, details['tr'], details['image_num'])] = pd.DataFrame(details, 
                                                columns=['onset', 
                                                        'duration', 
                                                        'trial_type'])
    return task_map
        

def _match_tasks(subject_num):
    task_map = _load_taskmap()
    func_path = WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/func/'
    for filename in os.listdir(func_path):
        
        if filename[-5:] != '.json':
            continue
        task_name = _parse_task_name(filename)
        tr, image = _get_metadata(subject_num, task_name)
        if (task_name, tr, image) not in task_map:
            print(f'sub-{subject_num} has a unique {task_name} task ({tr}, {image})')
            continue
        task_df: pd.DataFrame = task_map[(task_name, tr, image)]
        tsv_filename = filename[:-9] + 'events.tsv'
        
        with open(func_path + tsv_filename, 'w') as events_file:
            task_df.to_csv(events_file, sep = '\t', index=False)
        
if __name__ == '__main__':
    selected_subjects = [11]
    subject_nums = [str(i).zfill(3) for i in selected_subjects]
    for subject_num in subject_nums:
        _match_tasks(subject_num)