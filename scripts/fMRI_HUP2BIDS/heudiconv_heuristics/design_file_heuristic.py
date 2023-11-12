import re, os, pathlib

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    """
    For heudiconv: standard key template
    """
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """
    For heudiconv: selects only design files for conversion
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
        design_string = 'sub-{subject}/{session}/func/sub-{subject}_{session}_task-' + task_name + '_run-01_bold'
        design = create_key(design_string)
        info[design] = [s.series_id]
            
    return info