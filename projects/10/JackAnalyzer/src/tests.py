import unittest
from pathlib import Path

from file_util import is_jack_file

class TestFileUtil(unittest.TestCase):

    def test_is_jack_file_success(self):
        """Returns True when file extention is '.jack'."""
        file_path = Path('myFile.jack')
        output = is_jack_file(file_path)
        self.assertTrue(output)

    def test_is_jack_file_fail(self):
        """Returns False when file extention is not '.jack'."""
        file_path = Path('myFile.xml')
        output = is_jack_file(file_path)
        self.assertFalse(output)
