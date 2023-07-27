import os

data_folder = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_temps/source_data/'
bids_folder = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_data/'

#subjects with design files
def design_subjects():
    for subject in sorted(os.listdir(data_folder)):
        if 'design' not in os.listdir(data_folder + f'{subject}/ses-001'):
            continue
        print(subject)

def task_names():
    name_set = set()
    for subject in sorted(os.listdir(bids_folder)):
        if not os.path.isdir(bids_folder + f'{subject}/ses-001/func'):
            continue
        for file in os.listdir(bids_folder + f'{subject}/ses-001/func'):
            if file[-5:] != '.json':
                continue
            name_set.add(file.split('_')[2].split('-')[-1])
    for i in name_set:
        print(i)
        
def subject_has_task(task_name):
    for subject in sorted(os.listdir(bids_folder)):
        if not os.path.isdir(bids_folder + f'{subject}/ses-001/func'):
            continue
        for file in os.listdir(bids_folder + f'{subject}/ses-001/func'):
            if task_name in file:
                print(subject)
                break
            
if __name__ == '__main__':
    subject_has_task('binder')
        