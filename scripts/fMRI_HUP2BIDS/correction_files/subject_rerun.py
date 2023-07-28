import os, shutil, json, glob
from typing import List
import event_tsv_writer
import scripts.fMRI_HUP2BIDS.clean_files as clean_files

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def copy_subject(subject_id):
    """
    Copy BIDSified subject from location to bids_data folder, replacing old run
    """
    
    #clean subject folder
    clean_files.clear_subject(subject_id)
    
    #copy subject from location
    source_folder = WORKING_FOLDER_PATH + f'bids_temps/reruns/{subject_id}/ses-001'
   
    #TODO: fix hardcoding of session
    destination = WORKING_FOLDER_PATH + f'bids_data/{subject_id}/ses-001'
    
    #copy files
    shutil.copytree(source_folder, destination)

def run_heudiconv_data(subject_nums: List[str]) -> None:
    """
    Runs heudiconv on all subjects' data
    """
    command = ('heudiconv -d "' + WORKING_FOLDER_PATH
               + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"'
              + f' -o "{WORKING_FOLDER_PATH}bids_temps/reruns"' 
              + f' -f "{WORKING_FOLDER_PATH}hup_heuristic.py"'
              + f' -s {" ".join(subject_nums)} -ss 001 --overwrite -b')
    print(command)
    os.system(command)
    
def write_task_events(subject_num) -> None:
    """
    Run heudiconv on single-subject design files
    Read each design file and write to the tsvs
    """
    #TODO: update the path_info.json file for each subject
    with open(WORKING_FOLDER_PATH + 'path_info.json', 'w') as f:
        json.dump({'subject_id': subject_num, 
            'func_dir': WORKING_FOLDER_PATH + f'bids_data/sub-{subject_num}/ses-001/func'}, f)
    
    command = ('heudiconv -d "' + WORKING_FOLDER_PATH
               + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"'
              + f' -o "{WORKING_FOLDER_PATH}bids_temps/design_files"' 
              + f' -f "{WORKING_FOLDER_PATH}design_heuristic.py"'
              + f' -s {subject_num} -ss 001 --overwrite -b')
    print(command)
    os.system(command)
    
    event_tsv_writer.create_tsv()
    
    clean_files.clear_design_files()

if __name__ == '__main__':
    clean_files.clear_reruns()
    
    selected_subjects = [i for i in range(1, 37)]
    #subject_list = copy_subjects('bsc_subjects.txt')
    subject_list = [str(i).zfill(3) for i in selected_subjects]
    
    #run heudiconv for each subject
    run_heudiconv_data(subject_list)
    
    for subject_num in subject_list:
        subject_id = 'sub-' + subject_num
        #copy_subject(subject_id)
    
    #write events for each subject
    #for subject_num in subject_list:
        #write_task_events(subject_num)