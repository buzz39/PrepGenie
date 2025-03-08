import unittest
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass

    def tearDown(self):
        """Tear down test fixtures"""
        pass

    def test_environment_variables(self):
        """Test that required environment variables can be loaded"""
        required_vars = [
            'AZURE_VISION_ENDPOINT',
            'AZURE_VISION_KEY',
            'OPENAI_API_KEY'
        ]
        
        # This test will pass if the .env file exists
        self.assertTrue(os.path.exists('.env'), "Missing .env file")
        
        # Load environment variables from .env
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if all required variables are present
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        self.assertEqual(len(missing_vars), 0, 
                        f"Missing environment variables: {', '.join(missing_vars)}")

    def test_dependencies(self):
        """Test that all required dependencies can be imported"""
        required_packages = [
            'requests',
            'Pillow',
            'customtkinter',
            'python-dotenv',
            'pynput',
            'pyautogui',
            'keyboard',
            'openai',
            'httpx',
            'pystray'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        self.assertEqual(len(missing_packages), 0,
                        f"Missing packages: {', '.join(missing_packages)}")

if __name__ == '__main__':
    unittest.main() 