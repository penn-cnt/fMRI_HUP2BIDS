from folder_utils import get_folders, copy_subjects, clear_folder

SCRIPT_FOLDER, SOURCE_DATA_FOLDER, OUTPUT_FOLDER = get_folders()
copy_subjects(SCRIPT_FOLDER, SOURCE_DATA_FOLDER)

#run heudiconv on files to convert func, anat, fmap MRI dicoms

#address fieldmap jsons to func runs

#run heudiconv to get and read design files to fill events.tsv