from file_utils import setup_folders, get_folders, copy_subjects, clear_folder
from heudiconv_utils import run_heudiconv_data
import os

if __name__ == "__main__":
    #copy subject data to a temporary working folder
    # print("\nREMOVING PREVIOUS RUN\n")
    # setup_folders()
    # clear_folder("temporary_files/source_data")
    # clear_folder("temporary_files/design_files")
    # SCRIPT_FOLDER, SOURCE_DATA_FOLDER, OUTPUT_FOLDER = get_folders()
    # print("\nCOPYING SUBJECT DATA TO TEMPORARY FOLDER\n")
    # subject_ids = copy_subjects(SOURCE_DATA_FOLDER)
    
    subject_ids = [folder for folder in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temporary_files/source_data')) if folder[:4] == 'sub-'] 
    
    #run heudiconv on raw subject dicoms
    print("\nRUNNING HEUDICONV ON SUBJECT FOLDERS\n")
    # run_heudiconv_data(subject_ids, OUTPUT_FOLDER)
    run_heudiconv_data(subject_ids, '/mnt/leif/littlab/users/ezou626/fMRI_HUP2BIDS/scripts/fMRI_HUP2BIDS/output_files/dataset')

    #address fieldmap jsons to func runs

    #run heudiconv to get and read design files to fill events.tsv