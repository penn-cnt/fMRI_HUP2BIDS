import re, json

WORKING_FOLDER_PATH = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/'

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    """
    For heudiconv: standard run template
    """
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """
    For heudiconv: customizable selection of files
    """
    
    info = {}
    
    for s in seqinfo:
        
        #filter non-design files
        if s.dcm_dir_name != 'design':
            continue
        
        #match name with common protocol names
        match_object = re.search('ep2d_FMRI_90TR_', s.protocol_name)
        match_object2 = re.search('BOLD_', s.protocol_name)
        if not match_object and not match_object2:
            print("Failed to find match")
            continue
        
        #parse task name
        task_name = None
        if match_object:
            task_name = s.protocol_name[match_object.span()[1]:].lower()
        elif match_object2:
            task_name = s.protocol_name.split("_")[1].lower()
        
        #create key and add to info dict
        design_string = ('sub-{subject}/{session}/func/sub-{subject}_{session}_task-' 
            + task_name +'_run-01_bold') # type: ignore
        design = create_key(design_string)
        info[design] = [s.series_id]
        
        #TODO: add file based on subject number in path_info.json
        
        
        with open(WORKING_FOLDER_PATH + 'path_info.json', 'r') as f:
            subject_id = json.load(f)['subject_id']
            design_string = (f'sub-{subject_id}/ses-001/func/sub-{subject_id}_ses-001_task-' 
                + task_name +'_run-01_bold') # type: ignore
        
        #add design file to filelist
        with open(WORKING_FOLDER_PATH + 'bids_temps/design_files.txt', 'a') as file:
            file.write(WORKING_FOLDER_PATH + 'bids_temps/design_files/' + design_string + '\n')
        
    return info