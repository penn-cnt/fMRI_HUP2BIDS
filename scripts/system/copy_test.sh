#!/bin/bash

# Source directory where the folders are located
source_dir="/mnt/leif/littlab/data/Human_Data/language_fmri_data/source_data"

# Destination directory where you want to copy the folders
destination_dir="/mnt/leif/littlab/users/ezou626/fMRI_HUP2BIDS/user_data/small_test_data"

# List of folders you want to copy (space-separated)
folders_to_copy="sub-RID0102 sub-RID0194 sub-RID0380"

# Check if the source directory exists
if [ ! -d "$source_dir" ]; then
  echo "Source directory not found: $source_dir"
  exit 1
fi

# Check if the destination directory exists, if not, create it
if [ ! -d "$destination_dir" ]; then
  mkdir -p "$destination_dir"
fi

# Loop through the folders to copy
for folder in $folders_to_copy; do
  # Check if the folder exists in the source directory
  if [ -d "$source_dir/$folder" ]; then
    # Use 'cp' to recursively copy the folder to the destination directory
    cp -r "$source_dir/$folder" "$destination_dir"
    echo "Copied: $folder"
  else
    echo "Folder not found: $folder"
  fi
done

echo "Copy completed."