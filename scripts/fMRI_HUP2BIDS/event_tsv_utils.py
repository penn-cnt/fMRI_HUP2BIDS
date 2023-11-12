import pandas as pd
import nibabel as nib
import json, os
from typing import List

scenemem = {
    'data': {
        'onset': [0, 36, 72, 108, 144, 180, 216, 252, 288, 324, 360],
        'duration': [36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36],
        'trial_type': ['baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline'],
    },
    'tr': 3,
    'image_num': 132
}
#TODO: add binder info
binder = {
    'data': {
        'onset': [],
        'duration': [],
        'trial_type': [],
    },
    'name': 'binder',
    'tr': 3,
    'image_num': 140
}
presets = {'scenemem': scenemem}

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
DESIGN_FOLDER = os.path.join(SCRIPT_FOLDER, 'temporary_files/design_files')

def _parse_task_name(bids_file_path: str) -> str:
    """
    Parse design file path for task_name of form task-______
    """
    
    file_name = bids_file_path.split("/")[-1]
    task_name = file_name.split("_")[2].split('-')[-1]
    
    #XXX: parsed names may differ from heuristic, update this to switch to consistent names
    name_map = {'rhyming': 'rhyme', 
                'verbgeneration': 'verbgen', 
                'wordgeneration': 'wordgen'}
    
    if task_name in name_map:
        task_name = name_map[task_name]
    
    return task_name

    
def _read_design(design_nifti_path: str, design_json: str) -> pd.DataFrame:
    """
    Read design files and return pandas DataFrame containing information
    Refer to .json sidecard for TR to compute duration
    """
    
    nifti = nib.load(design_nifti_path)
    
    design_data = nifti.get_fdata() # type: ignore
    
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
    with open(design_json, 'r') as file:
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
    del nifti
    
    return task_dataframe, tr, images
        
def _get_subject_designs(subject_folder: str) -> dict:
    '''
    Gets all task designs from a subject
    ''' 
    for session in os.listdir(subject_folder):
        func_path = os.path.join(subject_folder, f'{session}/func')
    
    subject_tasks = {}
    for file in os.listdir(func_path):
        
        if not file[-7:] == '.nii.gz':
            continue
        
        filepath = os.path.join(func_path, file)
        taskname = _parse_task_name(file)
        
        design_df, tr, images = _read_design(filepath, filepath[:-7]+'.json')
        subject_tasks[(taskname, tr, images)] = design_df
        
    return subject_tasks

def _get_designs() -> dict:
    tasks = {}
    
    for subject in [i for i in os.listdir(DESIGN_FOLDER) if i[:3] == 'sub']:
        subject_folder = os.path.join(DESIGN_FOLDER, subject)
        for key, data in _get_subject_designs(subject_folder).items():
            if key not in tasks:
                tasks[key] = data
                
    for task in presets:
        preset = presets[task]
        data, tr, image_num, = preset['data'], preset['tr'], preset['image_num']
        if (task, tr, image_num) not in tasks:
            tasks[(task, tr, image_num)] = pd.DataFrame.from_dict(data)
    
    return tasks             

def _write_subject_tsvs(DATASET_PATH, LOG_PATH, tasks) -> List[str]:
    pass

def write_events_tsvs(DATASET_PATH, LOG_PATH, tasks) -> None:
    """

    """
    func_path_object = ""
    session = str(func_path_object).split("/")[-2]
    subject = str(func_path_object).split("/")[-3]
    with open("", 'r') as design_files:
        
        for design_file_path in design_files:
            
            # task_name = _parse_design_name(design_file_path)
            design_dataframe = _read_design(design_file_path)
            #TODO: fix hardcoding of run number
            
            file_name_1 = f'{subject}_{session}_{"task_name"}_run-01_events.tsv'
            file_path = str(func_path_object) + '/' + file_name_1
            design_dataframe.to_csv(file_path, sep = '\t')
            
            file_name_2 = f'{subject}_{session}_{"task_name"}_run-02_events.tsv'
            file_path = str(func_path_object) + '/' + file_name_2
            if os.path.isfile(file_path):
                design_dataframe.to_csv(file_path, sep = '\t', index = False)
                
if __name__ == '__main__':
    print(_get_designs())