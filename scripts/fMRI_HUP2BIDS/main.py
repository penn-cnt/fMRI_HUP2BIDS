from file_utils import setup_folders, get_folders, copy_subjects, clear_folder
from heudiconv_utils import run_heudiconv_data, remove_top_level_jsons, add_intended_for, run_heudiconv_design
from event_tsv_utils import write_events_tsvs

if __name__ == "__main__":
    #clean up old files and get folders
    print("\nSETTING UP FOLDERS FOR NEXT RUN\n")
    SCRIPT_FOLDER, SOURCE_DATA_FOLDER, OUTPUT_FOLDER, DATASET_FOLDER, LOGS_FOLDER = get_folders()
    setup_folders()

    #copy subject data to a temporary working folder
    print("\nCOPYING SUBJECT DATA TO TEMPORARY FOLDER\n")
    subject_ids = copy_subjects(SOURCE_DATA_FOLDER)
    
    # run heudiconv on raw subject dicoms
    print("\nRUNNING HEUDICONV ON SUBJECT FOLDERS\n")
    run_heudiconv_data(subject_ids, DATASET_FOLDER)
    remove_top_level_jsons(DATASET_FOLDER)
    add_intended_for(DATASET_FOLDER)

    # run heudiconv to get and read design files to fill events.tsv
    print("\nPOPULATING EVENTS.TSV FILES\n")
    run_heudiconv_design(subject_ids)
    write_events_tsvs(DATASET_FOLDER, LOGS_FOLDER)
