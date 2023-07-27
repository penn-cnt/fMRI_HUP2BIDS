import os, shutil

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def _clear_folder(folder) -> None:
    """
    Clears a folder of all files
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def clean_up(folder, remove_jsons = True) -> None:
    """
    Removes the temp files and past subject data from folders
    """
    #clear temps
    _clear_folder(WORKING_FOLDER_PATH + folder)
    
    #remove top-level task.json files
    if not remove_jsons:
        return
    for i in os.listdir(WORKING_FOLDER_PATH + 'bids_data'):
        if i[:4] != 'task':
            continue
        print(WORKING_FOLDER_PATH + 'bids_data/' + i)
        os.remove(WORKING_FOLDER_PATH + 'bids_data/' + i)
        
def reset_path_info():
    with open('/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/path_info.json', 'w') as f:
        f.write('{"subject_id": "001", "func_dir": null}')

def clear_outputs():
    clean_up('bids_outputs')
    
def clear_reruns():
    clean_up('bids_temps/reruns')
    
def clear_subject(subject_id):
    #TODO: fix hardcoding of session
    clean_up(f'bids_data/{subject_id}')

def clear_design_files():
    clean_up('bids_temps/design_files')
    try:
        os.remove('/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_temps/design_files.txt')
    except:
        pass