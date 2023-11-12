import nibabel as nib
import os
from scripts.fMRI_HUP2BIDS.clean_files import clean_up

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'


clean_up('bids_temps/design_files/test_dump', False)

subject_list = [9]
subject_nums = [str(i).zfill(3) for i in subject_list]
command = ('heudiconv -d "' + WORKING_FOLDER_PATH
               + 'bids_temps/source_data/sub-{subject}/ses-{session}/*/*"'
              + f' -o "{WORKING_FOLDER_PATH}bids_temps/design_files/test_dump"' 
              + f' -f "{WORKING_FOLDER_PATH}design_heuristic.py"'
              + f' -s {" ".join(subject_nums)} -ss 001 --overwrite -b')

print(command)
os.system(command)


