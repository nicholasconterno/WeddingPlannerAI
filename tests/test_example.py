import unittest
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import converse_with_vendor, get_summary, get_next_step_for_bride


class TestWeddingPlannerAI(unittest.TestCase):
    def test_converse_with_vendor(self):
        # Add your test logic here
        self.assertTrue(True)

    def test_get_summary(self):
        # Add your test logic here
        self.assertTrue(True)

    def test_get_next_step_for_bride(self):
        # Add your test logic here
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
