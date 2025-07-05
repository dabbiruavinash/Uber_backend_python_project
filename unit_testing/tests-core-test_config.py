# Test Config 

import unittest
import os
from core.config import settings

class TestConfig(unittest.TestCase):
       def test_default_values(self):
              self.assertEqual(settings.APP_ENV, "development")
              self.assertEqual(settings.DEFAULT_CURRENCY, "INR")
              self.assertEqual(settings.DEFAULT_TIMEZONE, "Asia/Kollkata")

       def test_environment_override(self):
              os.environ["APP_ENV"] = "production"
              from core.config import setting as prod_settings
              self.assertEqual(prod_setting.APP_ENV, "production")

if __name__ == '__main__'
     unittest.main()
