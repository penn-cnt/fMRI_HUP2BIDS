import pandas as pd
import nibabel as nib
import json, os
from typing import List

scenemem = {'onset': [0, 36, 72, 108, 144, 180, 216, 252, 288, 324, 360],
                     'duration': [36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36],
                     'trial_type':
                     ['baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline','stimulus','baseline'],
                     'tr': 3,
                     'image_num': 132}
#TODO: add binder info
binder = {'onset': [],
            'duration': [],
            'trial_type':[],
            'tr': 3,
            'image_num': 140}
presets = {'scenemem': scenemem}

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def _parse_design_name(design_file_path: str) -> str:
    """
    Parse design file path for task_name of form task-______
    """
    file_name = design_file_path.split("/")[-1] #should be last in path
    task_name = file_name.split("_")[2].split('-')[-1] #third in bids naming system
    
    #XXX: parsed names may differ from heuristic, update this to switch to consistent names
    name_map = {'rhyming': 'rhyme', 
                'verbgeneration': 'verbgen', 
                'wordgeneration': 'wordgen',}
    if task_name in name_map:
        task_name = name_map[task_name]
    
    return task_name

    
def _read_design(design_nifti: nib.nifti1, design_json: str) -> pd.DataFrame:
    """
    Read design files and return pandas DataFrame containing information
    Refer to .json sidecard for TR to compute duration
    """
    design_data = design_nifti.get_fdata() # type: ignore
    
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
    return task_dataframe

def _parse_task_name(event_tsv_filename: str):
    task_name = event_tsv_filename.split('_')[2].split('-')[1]
    return task_name

def _get_metadata(subject_num: str, task_name: str, run: str = '01'):
    tr, image_num = None, None
    func_path = WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/func/'
    filename = f'sub-{subject_num}_ses-001_task-{task_name}_run-{run}_bold.json'
    with open(func_path + filename, 'r') as file:
        metadata = json.load(file)
        tr = metadata['RepetitionTime']
        image_num = metadata['dcmmeta_shape'][3]
    return tr, image_num
        
def _get_designs(subject_num: str):
    '''
    Gets a map of task name to task event info
    ''' 
    func_path = WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/func/'
    
    task_map = {}
    for file in os.listdir(func_path):
        
        if not file[-10:] == 'events.tsv':
            continue
        
        filepath = func_path + file
        with open(filepath, 'r') as event_file:
            taskname = _parse_task_name(file)
            design_df = pd.read_csv(event_file, sep = '\t', index_col=False)
            task_map[taskname] = design_df
        
    return task_map

def _add_event_info(task_map: dict, task_name: str, tr: int, 
                    image_num: int, task_df: pd.DataFrame):
    if task_name not in task_map:
        task_map[task_name] = [(tr, image_num, task_df)]
        return
    for tr_i, image_num_i, task_df_i in task_map[task_name]:
        if tr_i == tr and image_num_i == image_num and task_df_i.equals(task_df):
            return
    task_map[task_name].append((tr, image_num, task_df))             

def unique_tasks(subject_nums: List[str]):
    '''
    Populate design_files folder with unique tsvs of events
    '''
    combined_task_map = {}
    unwritten_tasks = {}
    tasks_written = set()
    for subject_num in subject_nums:
        
        subject_task_map = _get_designs(subject_num)
        for task_name, task_df in subject_task_map.items():
            if (task_name == 'binder'):
                print(subject_num)
            #strange columns
            task_data: dict = task_df.to_dict('list')
            tr, image_num = _get_metadata(subject_num, task_name)
            
            if "TODO -- fill in rows and add more tab-separated columns if desired" in task_data:
                if task_name in unwritten_tasks:
                    if (tr, image_num) in unwritten_tasks[task_name]:
                        continue
                    unwritten_tasks[task_name].append((tr, image_num))
                    continue
                unwritten_tasks[task_name] = [(tr, image_num)]
                continue
            
            #weird extra column
            if "Unnamed: 0" in task_data:
                task_data.pop('Unnamed: 0')
                task_df = pd.DataFrame(task_data)
                
            _add_event_info(combined_task_map, task_name, tr, image_num, task_df)
            tasks_written.add((task_name, tr, image_num))
    for name, tr, image_num in tasks_written:
        try:
            unwritten_tasks[name].remove((tr,image_num))
        except:
            pass        
    return combined_task_map, {key: value for key, value in unwritten_tasks.items()}

def save_event_info(task_map: dict):
    design_folder = WORKING_FOLDER_PATH + 'bids_temps/design_files/'
    for task_name, task_versions in task_map.items():
        for index, (tr, image_num, task_df) in enumerate(task_versions):
            task_data: dict = task_df.to_dict('list')
            task_data['tr'] = tr
            task_data['image_num'] = image_num
            with open(design_folder + f'task-{task_name}_ver-{index}.json', 'w') as file:
                json.dump(task_data, file, indent=4)
                
def mark_todos(not_completed: dict):
    design_folder = WORKING_FOLDER_PATH + 'bids_temps/design_files/'
    for task_name, uncompleted_list in not_completed.items():
        for index, (tr, image_num) in enumerate(uncompleted_list):
            task_data = None
            if task_name in presets and presets[task_name]['tr'] == tr and presets[task_name]['image_num'] == image_num:
                task_data = presets[task_name]
            else:    
                task_data = {'onset': [], 'duration':[], 'trial_type': [], 'tr': tr, 'image_num': image_num}
            with open(design_folder + f'task-{task_name}_ver-{index}.json', 'w') as file:
                json.dump(task_data, file, indent=4)

def _write_tsvs(func_folder_path: str) -> None:
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