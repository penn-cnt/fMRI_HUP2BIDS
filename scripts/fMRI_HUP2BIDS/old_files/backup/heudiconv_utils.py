import os, json
from typing import List

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def run_heudiconv_data(subject_ids: List[str], output_folder: str) -> None:
    """
    Runs heudiconv on all subjects' data
    """
    src_path = os.path.join(SCRIPT_FOLDER, 'temporary_files/source_data/sub-{subject}/ses-{session}/*/*')
    command_function = lambda session: ('heudiconv -d "' + src_path + '"'
              + f' -o "{output_folder}"' 
              + f' -f "{SCRIPT_FOLDER}/heudiconv_heuristics/initial_hup_heuristic.py"'
              + f' -s {" ".join(map(lambda x: x[4:], subject_ids))} -ss {session:03} --overwrite -b')
    os.system(command_function(1))
    os.system(command_function(2))
    
def remove_top_level_jsons(output_folder) -> None:
    """
    Heudiconv generates top-level .json files for each task, which are not required for BIDS
    This function removes them.
    """
    for file in os.listdir(output_folder):
        if file[:4] != 'task' or file[-5:] != '.json':
            continue
        os.remove(os.path.join(output_folder, file))
        
def add_intended_for(output_folder):
    '''
    Fills IntendedFor fields of fmap json sidecar files
    '''
    for folder in output_folder:
        if folder == '.heudiconv':
            continue
        subject_id = folder
        subject_paths = [os.path.join(output_folder, f'{subject_id}/ses-001'), 
                         os.path.join(output_folder, f'{subject_id}/ses-002')]
        for subject_path in subject_paths:
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
                    img_list.append(f'{subject_paths}/func/{file}')
            
            if os.path.isdir(anat_path):
                for file in os.listdir(anat_path):
                    if not file[-7:] == '.nii.gz':
                        continue
                    img_list.append(f'{subject_paths}/anat/{file}')
                
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
                    
def run_heudiconv_design(subject_ids: List[str]) -> None:
    """
    Run heudiconv on single-subject design files
    Read each design file and write to the tsvs
    """
    src_path = os.path.join(SCRIPT_FOLDER, 'temporary_files/source_data/sub-{subject}/ses-{session}/*/*')
    command_function = lambda session: ('heudiconv -d "' + src_path + '"'
              + f' -o "{SCRIPT_FOLDER}/temporary_files/design_files"' 
              + f' -f "{SCRIPT_FOLDER}/heudiconv_heuristics/design_file_heuristic.py"'
              + f' -s {" ".join(map(lambda x: x[4:], subject_ids))} -ss {session:03} --overwrite -b')
    os.system(command_function(1))
    os.system(command_function(2))