import unittest
import os
from utils import create_dir_if_not_exists

class TestUtils(unittest.TestCase):
    
    def test_create_dir_if_not_exists(self):
        # Test creating a directory if it does not exist
        test_dir = "data/test_dir"
        if os.path.exists(test_dir):
            os.rmdir(test_dir)  # Ensure the directory doesn't exist before testing
        
        create_dir_if_not_exists(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        
        # Cleanup after test
        os.rmdir(test_dir)

if __name__ == '__main__':
    unittest.main()
