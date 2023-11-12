from file_utils import setup_folders, get_folders, copy_subjects, clear_folder
from heudiconv_utils import run_heudiconv_data, remove_top_level_jsons, add_intended_for, run_heudiconv_design
from event_tsv_utils import write_event_tsvs
import os

if __name__ == "__main__":
    #copy subject data to a temporary working folder
    # print("\nREMOVING PREVIOUS RUN\n")
    # setup_folders()
    # clear_folder("temporary_files/source_data")
    # clear_folder("temporary_files/design_files")
    # SCRIPT_FOLDER, SOURCE_DATA_FOLDER, OUTPUT_FOLDER = get_folders()
    OUTPUT_FOLDER = '/mnt/leif/littlab/users/ezou626/fMRI_HUP2BIDS/scripts/fMRI_HUP2BIDS/output_files' #hardcode
    DATASET_FOLDER = os.path.join(OUTPUT_FOLDER, 'dataset')
    LOGS_FOLDER = os.path.join(OUTPUT_FOLDER, 'logs')
    # print("\nCOPYING SUBJECT DATA TO TEMPORARY FOLDER\n")
    # subject_ids = copy_subjects(SOURCE_DATA_FOLDER)
    subject_ids = [folder for folder in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temporary_files/source_data')) if folder[:4] == 'sub-'] 
    
    # run heudiconv on raw subject dicoms
    # print("\nRUNNING HEUDICONV ON SUBJECT FOLDERS\n")
    # run_heudiconv_data(subject_ids, DATASET_FOLDER)
    # remove_top_level_jsons(DATASET_FOLDER)
    # add_intended_for(DATASET_FOLDER)

    # run heudiconv to get and read design files to fill events.tsv
    print("\nPOPULATING EVENTS.TSV FILES\n")
    # run_heudiconv_design(subject_ids)
    write_event_tsvs(DATASET_FOLDER, LOGS_FOLDER)
