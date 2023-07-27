import pandas as pd
import numpy as np
import json, os

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'
DATASET_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_data/'

def load_subject_map():
    '''
    Get sub_id -> rid mapping
    '''
    subject_map = None
    with open(WORKING_FOLDER_PATH + 'subject_map.json', 'r') as file:
        subject_map = json.load(file)
    return subject_map

def _fix_scans_tsv(replace_id):
    '''
    Change subject scans file
    '''
    if not os.path.isfile(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv'):
        return
    scan_info = pd.read_csv(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', sep='\t', index_col=False)
    new_row = lambda row: [row['filename'].replace(subject_id, replace_id), row['acq_time'], row['operator'], row['randstr']]
    change_id = lambda row: new_row(row) if subject_id in row['filename'] else row
    edited_info = scan_info.apply(change_id, axis=1, result_type='broadcast')
    with open(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', 'w') as file:
        edited_info.to_csv(file, sep = '\t')
    os.rename(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', DATASET_PATH + f'{subject_id}/ses-001/{replace_id}_ses-001_scans.tsv')
    
def _change_files(replace_id):
    folders = os.listdir(DATASET_PATH + replace_id + '/ses-001/') #change back to subject
    for folder in folders:
        folder_path = DATASET_PATH + f'{replace_id}/ses-001/{folder}/'
        if not os.path.isdir(folder_path):
            continue
        files = os.listdir(folder_path)
        for file in files:
            try:
                os.rename(folder_path + file, folder_path + file.replace('ses-001', 'ses-clinical001'))
            except:
                pass

def _fmap_intendedfor(replace_id):
    '''
    Fills IntendedFor fields of fmap jsons
    '''
    
    subject_path = WORKING_FOLDER_PATH + f'bids_data/{replace_id}/ses-001/'
    
    fmap_path = subject_path + 'fmap/'
    func_path = subject_path + 'func/'
    #anat_path = subject_path + 'anat/'
    
    if not os.path.isdir(fmap_path):
        return
    
    img_list = []
    
    if os.path.isdir(func_path):
        for file in os.listdir(func_path):
            if not file[-7:] == '.nii.gz':
                continue
            img_list.append(f'{replace_id}/ses-clinical001/func/{file}')
    
    # if os.path.isdir(anat_path):
    #     for file in os.listdir(anat_path):
    #         if not file[-7:] == '.nii.gz':
    #             continue
    #         img_list.append(f'{replace_id}/ses-001/anat/{file}')
        
    for file in os.listdir(fmap_path):
        if not file[-5:] == '.json':
            continue
        img_list = [f'bids::{img}' for img in img_list]
        
        json_dict = None
        with open(fmap_path + file, 'r') as json_file:
            print(replace_id)
            json_dict = json.load(json_file)
            
        json_dict['IntendedFor'] = img_list
        os.chmod(fmap_path + file, 0o777)
        
        with open(fmap_path + file, 'w') as json_file:
            json.dump(json_dict, json_file, indent = 4)

def change_subject(replace_id):
    #_change_scans_tsv(subject_id, replace_id)
    #try: _change_files(replace_id)
    #except: pass
    #_fmap_intendedfor(replace_id)
    #os.rename(DATASET_PATH + subject_id, DATASET_PATH + replace_id)
    try: os.rename(DATASET_PATH + replace_id + f'/ses-clinical001/{replace_id}_ses-001_scans.tsv', 
                   DATASET_PATH + replace_id + f'/ses-clinical001/{replace_id}_ses-clinical001_scans.tsv')
    except: pass
    
if __name__ == '__main__':
    subject_map = load_subject_map()
    # change_participants_tsv(subject_map)
    name_set = set()
    with open(WORKING_FOLDER_PATH + 'binder_task.txt', 'r') as file:
        for line in file:
            name_set.add(line[:-1])
    for subject_id in sorted(name_set): #change back to os.listdir
        replace_id = subject_map[subject_id]
        print(replace_id)
        # if os.path.isfile(DATASET_PATH + subject_id) or subject_id == '.heudiconv':
        #     continue
        # df = pd.read_csv(WORKING_FOLDER_PATH + f'bids_temps/reruns/{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', sep = '\t', index_col = False)
        # new_id = lambda x: x.replace(subject_id, replace_id).replace('ses-001', 'ses-clinical001')
        # fix_op = lambda x: 'n/a' if type(x) != str and np.isnan(x) else x
        # row_func = lambda row: [new_id(row['filename']), row['acq_time'], fix_op(row['operator']), row['randstr']]
        # df = df.apply(row_func, axis = 1, result_type='broadcast')
        
        # with open(DATASET_PATH + f'{replace_id}/ses-001/{replace_id}_ses-001_scans.tsv', 'w') as file:
        #     df.to_csv(DATASET_PATH + f'{replace_id}/ses-001/{replace_id}_ses-001_scans.tsv', index=False, sep='\t')
        #change_subject(replace_id)
        
        # with open(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', 'w') as file:
        #     config.to_csv(file, sep = '\t', index = False)
    #     # if subject_id not in subject_map:
    #     #     continue
    #     replace_id = subject_map[subject_id]
    #     #change_subject(subject_id, replace_id)
    #     _fmap_intendedfor(replace_id)