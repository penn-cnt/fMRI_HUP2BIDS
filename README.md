# HUP2BIDS
## Convert HUP scans to BIDS format with Heudiconv

## How to Use
First, create a new Python 3 environment or activate one with the following packages installed:

- nibabel
- heudiconv
- pandas

Navigate to ./scripts/fMRI_HUP2BIDS and run python3 -m main, and type the absolute paths to the folders requested. The source data folder refers to the folder storing the individual subject data folders with RIDs. If the output data folder does not exist, one will be created.

If you find any bugs or issues, please email ezou626@seas.upenn.edu.