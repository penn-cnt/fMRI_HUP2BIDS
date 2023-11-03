import unittest
import os
import file_utils
        
class TestGetFolders(unittest.TestCase):
    def get_folders(self):
        SCRIPT_FOLDER, SOURCE_DATA_FOLDER, OUTPUT_FOLDER = file_utils.get_folders()
        self.assertEquals(SCRIPT_FOLDER, 
            '/mnt/leif/littlab/users/ezou626/fMRI_HUP2BIDS/scripts/fMRI_HUP2BIDS')
        print(SOURCE_DATA_FOLDER, OUTPUT_FOLDER)
    
if __name__ == '__main__':
    unittest.main()