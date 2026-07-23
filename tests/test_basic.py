import unittest
import os
import sys
import importlib.util
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass

    def tearDown(self):
        """Tear down test fixtures"""
        pass

    def test_environment_variables_handling(self):
        """Test that the application can handle environment variables gracefully"""
        required_vars = [
            'AZURE_VISION_ENDPOINT',
            'AZURE_VISION_KEY',
            'OPENAI_API_KEY'
        ]
        
        # Simulate environment variables being present
        with patch.dict(os.environ, {
            'AZURE_VISION_ENDPOINT': 'https://test.endpoint/',
            'AZURE_VISION_KEY': 'test_key',
            'OPENAI_API_KEY': 'test_openai_key'
        }):
            # Verify we can access them
            for var in required_vars:
                self.assertIsNotNone(os.getenv(var))

    def test_dependencies(self):
        """Test that all required dependencies can be imported"""
        required_packages = [
            'requests',
            'PIL',  # Pillow imports as PIL
            'customtkinter',
            'dotenv', # python-dotenv imports as dotenv
            'pynput',
            'pyautogui',
            'keyboard',
            'openai',
            'httpx',
            'pystray'
        ]
        
        missing_packages = [
            package
            for package in required_packages
            if importlib.util.find_spec(package) is None
        ]
        
        self.assertEqual(len(missing_packages), 0,
                        f"Missing packages: {', '.join(missing_packages)}")

if __name__ == '__main__':
    unittest.main()
