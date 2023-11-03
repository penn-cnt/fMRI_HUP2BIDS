import os, json
from typing import List

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def run_heudiconv_data(subject_ids: List[str], output_folder: str) -> None:
    """
    Runs heudiconv on all subjects' data
    """
    base_path = os.path.join(SCRIPT_FOLDER, 'temporary_files/source_data/{subject}/ses-{session}/*/*')
    command_function = lambda session: ('heudiconv -d "' + base_path + '"'
              + f' -o "{output_folder}"' 
              + f' -f "{SCRIPT_FOLDER}/heudiconv_heuristics/initial_hup_heuristic.py"'
              + f' -s {" ".join(subject_ids)} -ss {session:03} --overwrite -b')
    os.system(command_function(1))
    os.system(command_function(2))
    
def write_task_events(subject_id) -> None:
    """
    Run heudiconv on single-subject design files
    Read each design file and write to the tsvs
    """
    #TODO: update the path_info.json file for each subject
    with open(SCRIPT_FOLDER + 'path_info.json', 'w') as f:
        f.write(json.dumps({'subject_id': subject_id, 
                            'func_dir': SCRIPT_FOLDER + f'/bids_data/{subject_id}/ses-001/func'}))
    
    command = ('heudiconv -d "' + SCRIPT_FOLDER
               + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"'
              + f' -o "{SCRIPT_FOLDER}/bids_temps/design_files"' 
              + f' -f "{SCRIPT_FOLDER}/design_heuristic.py"'
              + f' -s {subject_id[-3:]} -ss 001 --overwrite -b')
    
    os.system(command)
    
def remove_top_level_jsons(target_folder) -> None:
    """
    Heudiconv generates top-level .json files for each task, which are not required for BIDS
    This function removes them
    """
    for file in os.listdir(target_folder):
        if file[:4] != 'task' or file[-5:] != '.json':
            continue
        os.remove(os.path.join(target_folder, file))