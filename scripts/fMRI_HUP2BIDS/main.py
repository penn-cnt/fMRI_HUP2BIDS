import os, shutil, json, glob
from typing import List
import event_tsv_writer
import clean

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def _copy_from_location(subject_path: str, subject_id: str) -> None:
    """
    Copies subject data from original location given HUP subject id and path to subject
    """
    
    #get folder name
    folder_name = subject_path.split('/')[-1]
    
    #TODO: fix hardcoding of session
    destination = WORKING_FOLDER_PATH + f'bids_temps/source_data/{subject_id}/ses-001/{folder_name}'
    
    #copy files
    shutil.copytree(subject_path, destination)

def copy_subjects(subject_file):
    """
    Copy subjects from location to destination folder
    """
    
    subject_map = {}
    
    #copy each subject from location
    source_folder = '/mnt/leif/littlab/data/Human_Data/language_fmri_data/source_data/'
    subject_list = []
    os.mkdir(WORKING_FOLDER_PATH + f'bids_temps/source_data/')
    with open(WORKING_FOLDER_PATH + subject_file, 'r') as subjects:
        for index, subject in enumerate(subjects):
            #get id
            subject_num = str(index + 1).zfill(3)
            subject_list.append(subject_num)
            subject_id = f'sub-{subject_num}'
            
            #make subject directory
            os.mkdir(WORKING_FOLDER_PATH + f'bids_temps/source_data/{subject_id}/')
            
            #TODO: fix hardcoding of sessions
            os.mkdir(WORKING_FOLDER_PATH + f'bids_temps/source_data/{subject_id}/ses-001/')
            
            #copy files
            for directory in glob.glob(source_folder + f'{subject[:-1]}/ses*/mr*/*'):
                _copy_from_location(directory, subject_id)
                
            #update subject map
            subject_map[subject_id] = subject[:-1]
    
    #save the subject map to match each patient to BIDS folder
    with open(WORKING_FOLDER_PATH + 'bids_outputs/subject_map.json', 'w') as file:
        json.dump(subject_map, file)
        
    return subject_list

def get_map(subject_file):
    subject_map = {}
    with open(WORKING_FOLDER_PATH + subject_file, 'r') as subjects:
        for index, subject in enumerate(subjects):
            #get id
            subject_num = str(index + 1).zfill(3)
            subject_id = f'sub-{subject_num}'
            
            #update subject map
            subject_map[subject_id] = subject[:-1]
    
    #save the subject map to match each patient to BIDS folder
    with open(WORKING_FOLDER_PATH + 'bids_outputs/subject_map.json', 'w') as file:
        json.dump(subject_map, file)

def run_heudiconv_data(subject_ids: List[str], base_path = WORKING_FOLDER_PATH + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"') -> None:
    """
    Runs heudiconv on all subjects' data
    """
    command = ('heudiconv -d "' + base_path + '"'
              + f' -o "{WORKING_FOLDER_PATH}bids_temps/new_folder"' 
              + f' -f "{WORKING_FOLDER_PATH}design_heuristic.py"'
              + f' -s {" ".join(("RID0" + id[-3:] for id in subject_ids))} --overwrite -b')
    print(command)
    os.system(command)
            
def write_task_events(subject_id) -> None:
    """
    Run heudiconv on single-subject design files
    Read each design file and write to the tsvs
    """
    #TODO: update the path_info.json file for each subject
    with open(WORKING_FOLDER_PATH + 'path_info.json', 'w') as f:
        f.write(json.dumps({'subject_id': subject_id, 
                            'func_dir': WORKING_FOLDER_PATH + f'bids_data/sub-{subject_id}/ses-001/func'}))
    
    command = ('heudiconv -d "' + WORKING_FOLDER_PATH
               + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"'
              + f' -o "{WORKING_FOLDER_PATH}bids_temps/design_files"' 
              + f' -f "{WORKING_FOLDER_PATH}design_heuristic.py"'
              + f' -s {subject_id[-3:]} -ss 001 --overwrite -b')
    print(command)
    os.system(command)
    
    #event_tsv_writer.create_tsv()
    
    #clean.clean_up('bids_temps/design_files', False)
    # try:
    #     os.remove(WORKING_FOLDER_PATH + 'bids_temps/design_files.txt')
    # except:
    #     pass
    
def add_intendedfor(subject_num):
    '''
    Fills IntendedFor fields of fmap jsons
    '''
    
    subject_path = WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/'
    
    fmap_path = subject_path + 'fmap/'
    func_path = subject_path + 'func/'
    anat_path = subject_path + 'anat/'
    
    if not os.path.isdir(fmap_path):
        return
    
    img_list = []
    
    if os.path.isdir(func_path):
        for file in os.listdir(func_path):
            if not file[-7:] == '.nii.gz':
                continue
            img_list.append(f'sub-{subject_num}/ses-001/func/{file}')
    
    if os.path.isdir(anat_path):
        for file in os.listdir(anat_path):
            if not file[-7:] == '.nii.gz':
                continue
            img_list.append(f'sub-{subject_num}/ses-001/anat/{file}')
        
    for file in os.listdir(fmap_path):
        if not file[-5:] == '.json':
            continue
        img_list = [f'bids::{img}' for img in img_list]
        
        json_dict = None
        with open(fmap_path + file, 'r') as json_file:
            json_dict = json.load(json_file)
            
        json_dict['IntendedFor'] = img_list
        os.chmod(fmap_path + file, 0o777)
        
        with open(fmap_path + file, 'w') as json_file:
            json_file.write(json.dumps(json_dict))

if __name__ == "__main__":
    
    subject_list = copy_subjects('bsc_subjects.txt')
    get_map('bsc_subjects.txt')
    with open(WORKING_FOLDER_PATH + 'bids_outputs/subject_map.json', 'r') as file:
        subject_map = json.load(file)
    clean.clean_up('bids_temps/new_folder', False)
    subject_list = [subject_map['sub-' + str(i).zfill(3)] for i in [1, 9, 18, 24, 25, 26, 31, 33, 34, 35, 36]]
    #run heudiconv for each subject
    run_heudiconv_data(subject_list, '/mnt/leif/littlab/data/Human_Data/language_fmri_data/source_data/sub-{subject}/ses-*/mr*/*/*')

    
    for subject_num in subject_list:
        write_task_events(subject_num)
        add_intendedfor(subject_num)