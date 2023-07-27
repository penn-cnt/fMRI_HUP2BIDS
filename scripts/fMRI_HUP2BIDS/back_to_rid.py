import pandas as pd
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

def change_participants_tsv(subject_map):
    '''
    Change toplevel participants.tsv file
    '''
    participants_info = pd.read_csv(DATASET_PATH + 'participants.tsv', sep='\t', index_col=False)
    new_row = lambda row: [subject_map[row['participant_id']], row['age'], row['sex'], row['group']]
    change_id = lambda row: new_row(row) if row['participant_id'] in subject_map else row
    edited_info = participants_info.apply(change_id, axis=1, result_type='broadcast')
    with open(DATASET_PATH + 'participants.tsv', 'w') as file:
        edited_info.to_csv(file, sep = '\t', index=False)

def _change_scans_tsv(subject_id, replace_id):
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
    
def _change_files(subject_id, replace_id):
    folders = os.listdir(DATASET_PATH + subject_id + '/ses-001/')
    for folder in folders:
        folder_path = DATASET_PATH + f'{subject_id}/ses-001/{folder}/'
        if not os.path.isdir(folder_path):
            continue
        files = os.listdir(folder_path)
        for file in files:
            try:
                os.rename(folder_path + file, folder_path + file.replace(subject_id, replace_id))
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
            img_list.append(f'{replace_id}/ses-001/func/{file}')
    
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
            json_dict = json.load(json_file)
            
        json_dict['IntendedFor'] = img_list
        os.chmod(fmap_path + file, 0o777)
        
        with open(fmap_path + file, 'w') as json_file:
            json_file.write(json.dumps(json_dict))

def change_subject(subject_id, replace_id):
    _change_scans_tsv(subject_id, replace_id)
    _change_files(subject_id, replace_id)
    _fmap_intendedfor(replace_id)
    os.rename(DATASET_PATH + subject_id, DATASET_PATH + replace_id)
    
if __name__ == '__main__':
    subject_map = load_subject_map()
    # change_participants_tsv(subject_map)
    for subject_id in subject_map: #change back to os.listdir
        if os.path.isfile(DATASET_PATH + subject_id) or subject_id == '.heudiconv':
            continue
        df = None
        with open(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', 'r') as file:
            lines = file.readlines()
            titles = lines[0][2:-2].split('\t')
            columns = [[] for _ in lines[0][2:-2].split('\t')]
            for line in lines[1:]:
                for i in range(4):
                    columns[i].append(line[3:-2].split('\t')[i])
            map = {i:j for i, j in zip(titles, columns)}
            df = pd.DataFrame(map, columns = titles)
        
        with open(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', 'w') as file:
            df.to_csv(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', index=False, sep='\t')
        # with open(DATASET_PATH + f'{subject_id}/ses-001/{subject_id}_ses-001_scans.tsv', 'w') as file:
        #     config.to_csv(file, sep = '\t', index = False)
    #     # if subject_id not in subject_map:
    #     #     continue
    #     replace_id = subject_map[subject_id]
    #     #change_subject(subject_id, replace_id)
    #     _fmap_intendedfor(replace_id)