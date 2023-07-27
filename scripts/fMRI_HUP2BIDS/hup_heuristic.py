import os
import json

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# structurals
t1w1 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_run-01_T1w')
t1w2 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_run-02_T1w')
t2w1 = create_key(
     'sub-{subject}/{session}/anat/sub-{subject}_{session}_run-01_T2w')
t2w2 = create_key(
     'sub-{subject}/{session}/anat/sub-{subject}_{session}_run-02_T2w')
t2_2d = create_key(
     'sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-2D_T2w')
t2_cor = create_key(
     'sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-coronal_T2w')
flair = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_FLAIR')
flair2 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-3D_FLAIR')
tof1 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_angio')
tof2 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-cor_angio')
tof3 = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-sag_angio')

# task fMRI
object_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-object_run-01_bold')
object_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-object_run-02_bold')
rhyme_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rhyme_run-01_bold')
rhyme_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rhyme_run-02_bold')
scenemem_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-scenemem_run-01_bold')
scenemem_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-scenemem_run-02_bold')
sentence_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-sentence_run-01_bold')
sentence_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-sentence_run-02_bold')
wordgen_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-wordgen_run-01_bold')
wordgen_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-wordgen_run-02_bold')
binder_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-binder_run-01_bold')
binder_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-binder_run-02_bold')
verbgen_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-verbgen_run-01_bold')
verbgen_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-verbgen_run-02_bold')
auditory_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-auditory_run-01_bold')
auditory_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-auditory_run-02_bold')
picture_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-picture_run-01_bold')
picture_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-picture_run-02_bold')
rest_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-01_bold')
rest_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-02_bold')

# ASL scans
asl = create_key(
     'sub-{subject}/{session}/perf/sub-{subject}_{session}_asl')
m0 = create_key(
    'sub-{subject}/{session}/perf/sub-{subject}_{session}_m0scan')
mean_perf = create_key(
    'sub-{subject}/{session}/perf/sub-{subject}_{session}_mean-perfusion')

# Diffusion
dwi = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi')

# Field maps
b0_mag = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')
b0_phase = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
pe_rev = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-multishell_dir-j_epi')
bold_tu = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_dir-j_epi')


def infotodict(seqinfo):
    print("\n\n\n\nHEURISTIC CALL\n\n\n\n")
    skipped = set()
    last_run = len(seqinfo)

    info = {t1w1:[], t1w2:[], t2w1:[],t2w2:[], t2_2d:[], t2_cor:[],flair:[], flair2:[], tof1: [],
            tof2: [], tof3: [], pe_rev: [],dwi:[],object_run1: [], object_run2: [],
            rhyme_run1: [],rhyme_run2: [],scenemem_run1: [], scenemem_run2: [], sentence_run1: [],
            sentence_run2: [],wordgen_run1: [], wordgen_run2: [],
            picture_run1: [], picture_run2: [], auditory_run1: [], auditory_run2: [], binder_run1: [],
            binder_run2:[],verbgen_run1: [], verbgen_run2: [], rest_run1: [], rest_run2: [],
            bold_tu: [],asl: [], m0: [], mean_perf: [], b0_phase: [], b0_mag: []}

# sometimes patients struggle with a task the first time around (or something
# else goes wrong and often some tasks are repeated. This function accomodates
# the variable number of task runs
    def get_both_series(key1, key2, s):
         if len(info[key1]) == 0:
             info[key1].append(s.series_id)
         else:
             info[key2].append(s.series_id)

# this doesn't need to be a function but using it anyway for aesthetic symmetry
# with above function
    def get_series(key, s):
            info[key].append(s.series_id)

    MINIMUM_IMAGES = 50
    
    for s in seqinfo:
        if "mean_&_t-maps" == s.series_description.lower() or s.is_derived:
            skipped.add(s.dcm_dir_name)
            continue
        protocol = s.protocol_name.lower()
        if any(id in protocol for id in ["t1w", "t1", "mprage_t"]) and 'cor' not in protocol and 'true' not in protocol and 'sag' not in protocol:
            get_both_series(t1w1, t1w2, s)
        elif "t2w_spc" in protocol or "t2 axial" in protocol:
            get_both_series(t2w1, t2w2,s)
        elif "t2_2d" in protocol:
            get_series(t2_2d, s)
        elif "t2_tse_coronal" in protocol or 't2 cor' in protocol:
            get_series(t2_cor, s)
        elif "tra_flair" in protocol:
            get_series(flair,s)
        elif "flair" in protocol and "3d" in protocol or 't2 flair' in protocol or 't2 flair cor' in protocol or 'axial flair' in protocol or 't2_flair' in protocol:
            get_series(flair2,s)

        elif "tof" in protocol:
            if "COR" in s.series_description:
                get_series(tof2,s)
            elif "SAG" in s.series_description:
                get_series(tof3,s)
            else:
                get_series(tof1,s)

        elif "topup" in protocol and "BOLD" not in s.series_description:
            get_series(pe_rev, s)
        elif ("multishell" in protocol or 'mddw dti' in protocol) and not s.is_derived:
            get_series(dwi, s)
        elif ("object" in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(object_run1,object_run2,s)
        elif ("rhyming" in protocol or 'rhyme' in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(rhyme_run1,rhyme_run2,s)
        elif ("scenemem" in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(scenemem_run1,scenemem_run2,s)
        elif ("sentence" in protocol or "sentcomp" in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(sentence_run1, sentence_run2, s)
        elif ("wordgen" in protocol or "word_gen" in protocol  or 'word gen' in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(wordgen_run1,wordgen_run2,s)
        elif ("auditory" in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(auditory_run1,auditory_run2,s)
        elif ("picture" in protocol  or "pic_naming" in protocol  or 'pic naming' in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(picture_run1,picture_run2,s)
        elif "binder" in protocol:
            get_both_series(binder_run1, binder_run2,s)
        elif ("verbgen" in protocol or 'verb gen' in protocol) and s.series_files > MINIMUM_IMAGES:
            get_both_series(verbgen_run1, verbgen_run2,s)
        elif "restBOLD" in s.series_description and "asl" not in protocol:
            get_both_series(rest_run1, rest_run2, s)
        elif "topup" in protocol and "MULTISHELL" not in s.series_description:
            get_series(bold_tu, s)

        elif "spiral" in protocol:
            skipped.add(s.dcm_dir_name)
            if s.series_description.endswith("_ASL"):
                get_series(asl,s)
            elif s.series_description.endswith("_M0"):
                get_series(m0,s)
            elif s.series_description.endswith("_MeanPerf"):
                get_series(mean_perf,s)

        
        elif "b0" in protocol:
            if "P" in s.image_type:
                get_series(b0_phase,s)
            elif "M" in s.image_type:
                get_series(b0_mag,s)
        else:
            skipped.add(s.dcm_dir_name)
            continue
    
    config_info = None
    with open(os.path.dirname(__file__) + '/path_info.json', 'r') as f:
        config_info = json.load(f)

    subject = config_info["subject_id"]
    out_dir = '/mnt/leif/littlab/users/ezou626/Q1_LFMRI/code/bids_utils/bids_outputs/'

    config_info['subject_id'] = str(int(config_info['subject_id']) + 1).zfill(3)

    with open(os.path.dirname(__file__) + '/path_info.json', 'w') as f:
        json.dump(config_info, f)
    
    try:
        os.mkdir(out_dir)
    except:
        pass
    with open(out_dir + f'report_{subject}.txt', 'w') as file:
        file.write("Skipped Series:\n")
        for skipped_series in skipped:
            file.write(skipped_series + '\n')
        file.write('\n')
    
    return info

MetadataExtras = {
   b0_phase: {
       "EchoTime1": 0.00507,
       "EchoTime2": 0.00753
   },
   asl: {
   "PulseSequenceType": "3D_SPIRAL",
       "PulseSequenceDetails" : "WIP" ,
       "RepetitionTime":4.2,
       "LabelingType": "PCASL",
       "LabelingDuration": 1.8,
       "PostLabelingDelay": 1.8,
       "BackgroundSuppression": True,
       "BackgroundSuppressionNumberPulses": 2,
       "M0": "*_m0scan.nii",
       "LabelingOrientation":"transversal",
       "LabelingDistance":105,
       "LabelingPulseAverageGradient": 10,
       "LabelingPulseMaximumGradient": 80,
       "VascularCrushing": False,
       "PulseDuration": 0.0005,
       "LabelingPulseInterval": 0.00038,
       "PCASLType":"unbalanced",
       "LabelingEfficiency":0.72},
     binder_run1: {
     "FullTaskName": "Binder Semantic Decision"},
     binder_run2: {
     "FullTaskName": "Binder Semantic Decision"},
     object_run1: {
     "FullTaskName": "Object Naming"},
     object_run2: {
     "FullTaskName": "Object Naming"},
     rhyme_run1: {
     "FullTaskName": "Rhyme Matching"},
     rhyme_run2: {
     "FullTaskName": "Rhyme Matching"},
     scenemem_run1: {
     "FullTaskName": "Scene Memory"},
     scenemem_run2: {
     "FullTaskName": "Scene Memory"},
     sentence_run1: {
     "FullTaskName": "Sentence Completion"},
     sentence_run2: {
     "FullTaskName": "Sentence Completion"},
     verbgen_run1: {
     "FullTaskName": "Verb Generation"},
     verbgen_run2: {
     "FullTaskName": "Verb Generation"},
     auditory_run1: {
     "FullTaskName": "Audio Word Lists"},
     auditory_run2: {
     "FullTaskName": "Audio Word Lists"},
     picture_run1: {
     "FullTaskName": "Picture Naming"},
     picture_run2: {
     "FullTaskName": "Picture Naming"},
     wordgen_run1: {
     "FullTaskName": "Word Generation"},
     wordgen_run2: {
     "FullTaskName": "Word Generation"},
}