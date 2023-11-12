import os, shutil

def clear_folder(script_folder, folder_name) -> None:
    """
    Clears a folder of all files
    """
    folder = script_folder + folder_name
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        
def remove_top_level_jsons(script_folder):
    """
    Heudiconv generates top-level .json files for each task, which are not required
    This function removes them
    """
    for i in os.listdir(script_folder + 'bids_data'):
        if i[:4] != 'task':
            continue
        print(script_folder + 'bids_data/' + i)
        os.remove(script_folder + 'bids_data/' + i)
        
def reset_path_info():
    with open('/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/path_info.json', 'w') as f:
        f.write('{"subject_id": "001", "func_dir": null}')

def clear_outputs():
    clear_folder('bids_outputs')
    
def clear_reruns():
    clear_folder('bids_temps/reruns')
    
def clear_subject(subject_id):
    #TODO: fix hardcoding of session
    clear_folder(f'bids_data/{subject_id}')

def clear_design_files():
    clear_folder('bids_temps/design_files')
    try:
        os.remove('/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_temps/design_files.txt')
    except:
        pass