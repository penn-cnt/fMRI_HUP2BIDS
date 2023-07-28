import unittest
import os

class TestPathValidity(unittest.TestCase):
    def test_src_folder(self):
        SRC_FOLDER = os.path.dirname(os.path.realpath(__file__))
        self.assertEquals(SRC_FOLDER, 
            '/mnt/leif/littlab/users/ezou626/fMRI_HUP2BIDS/unit_tests/machine_level')
    
if __name__ == '__main__':
    unittest.main()