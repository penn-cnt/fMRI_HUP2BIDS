import os, shutil, glob

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def setup_folders() -> None:
    for folder in ['temporary_files', 'config_files', 'output_files']:
        if not os.path.isdir(SCRIPT_FOLDER + folder):
            os.mkdir(SCRIPT_FOLDER + folder)

def get_folders() -> (str, str, str):
    source_directory = input('Path to the source data directory: ')
    if not os.path.isdir(source_directory):
        print('Provided path is not a directory')
        exit()
    output_directory = input('Path to the output directory: ')
    return SCRIPT_FOLDER, source_directory, output_directory

def copy_subject(subject: str, source_folder: str) -> None:
    """
    Copies subject data from original location given HUP subject id and path to subject
    """
    for directory in glob.glob(source_folder + f'{subject}/ses*/mr*/*'):
        folder_name = directory.split()[-1]
        #TODO: fix hardcoding of session
        destination = SCRIPT_FOLDER + f'temporary_files/source_data/{subject}/ses-001/{folder_name}'
        shutil.copytree(directory, destination)
    
def copy_subjects(source_folder: str) -> [str]:
    """
    Copy subjects from location to destination folder
    """
    #source_folder = '/mnt/leif/littlab/data/Human_Data/language_fmri_data/source_data/'
    new_data_folder = SCRIPT_FOLDER + '/temporary_files/source_data/'
    if not os.path.isdir(new_data_folder):
        os.mkdir(new_data_folder)
    
    subjects = [folder for folder in os.listdir(source_folder) if folder[:4] == 'sub-']  
    for subject in subjects:
        os.mkdir(SCRIPT_FOLDER + f'/temporary_files/source_data/{subject}/')
        #TODO: fix hardcoding of sessions
        os.mkdir(SCRIPT_FOLDER + f'/temporary_files/source_data/{subject}/ses-001/')
        copy_subject(SCRIPT_FOLDER, source_folder, subject)
        
    return subjects

def clear_folder(folder_name) -> None:
    """
    Clears a folder of all files
    """
    folder = os.path.join(SCRIPT_FOLDER, folder_name)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def remove_top_level_jsons(target_folder) -> None:
    """
    Heudiconv generates top-level .json files for each task, which are not required for BIDS
    This function removes them
    """
    for file in os.listdir(target_folder):
        if file[:4] != 'task' or file[-5:] != '.json':
            continue
        os.remove(os.path.join(target_folder, file))