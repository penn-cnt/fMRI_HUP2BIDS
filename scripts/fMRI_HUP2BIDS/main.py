import os, os.path as path
from sys import exit

#sketch
#get source directory and output directory
source_directory = input('Path to the source data directory: ')
if not path.isdir(source_directory):
    print('Provided path is not a directory')
    exit()
output_directory = input('Path to the output directory: ')

#copy dicom files and structure to temp

#run heudiconv on files to convert func, anat, fmap MRI dicoms

#address fieldmap jsons to func runs

#run heudiconv to get and read design files to fill events.tsv