import os, shutil, glob
from typing import List
from multiprocessing import Pool

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def setup_folders() -> None:
    """
    Create/clear working folders required for script
    """
    for folder_name in ['temporary_files', 'config_files', 'temporary_files/design_files', 'temporary_files/source_data']:
        folder = os.path.join(SCRIPT_FOLDER, folder_name)
        if not os.path.isdir(folder):
            os.mkdir(folder)
    clear_folder("temporary_files/source_data")
    clear_folder("temporary_files/design_files")

def get_folders() -> (str, str, str):
    """
    Returns input, output, and current directories
    """
    source_directory = input('Path to the source data directory: ')
    if not os.path.isdir(source_directory):
        print('Provided path is not a directory')
        exit()
    output_directory = input('Path to the output directory: ')
    if not os.path.isdir(output_directory):
        print('Creating output directory since it does not exist')
        os.mkdir(output_directory)
    dataset_directory = os.path.join(output_directory, 'dataset')
    log_directory = os.path.join(output_directory, 'logs')
    if not os.path.isdir(log_directory):
        os.mkdir(log_directory)
    return SCRIPT_FOLDER, source_directory, output_directory, dataset_directory, log_directory

def copy_subject(subject_id: str, subject_folder: str, source_folder: str) -> None:
    """
    Copies subject data from original location given HUP subject id and path to subject
    """
    session_names = glob.glob(source_folder + f'/{subject_id}/ses*')
    
    for i, session in enumerate(session_names):
        session_folder = os.path.join(subject_folder, f'ses-{i+1:03}')
        os.mkdir(session_folder)
        
        for folder_path in glob.glob(session + '/mr*/*'):
            folder_name = folder_path.split('/')[-1]
            destination = os.path.join(session_folder, folder_name)
            shutil.copytree(folder_path, destination)
            
    return None
    
def copy_subjects(source_folder: str) -> List[str]:
    """
    Copy subjects from location to destination folder
    """
    new_data_folder = os.path.join(SCRIPT_FOLDER, 'temporary_files/source_data')
    if not os.path.isdir(new_data_folder):
        os.mkdir(new_data_folder)
    
    subjects = [folder for folder in os.listdir(source_folder) if folder[:4] == 'sub-']
    subject_folders = []
    for subject in subjects:
        subject_folder = os.path.join(new_data_folder, subject)
        subject_folders.append(subject_folder)
        os.mkdir(subject_folder)
    
    sources = [source_folder for i in range(len(subjects))]
        
    with Pool(5) as p:
        r = p.starmap_async(copy_subject, list(zip(subjects, subject_folders, sources)))
        r.wait()
        
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