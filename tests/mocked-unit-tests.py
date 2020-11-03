import unittest
import unittest.mock as mock
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

class TestCase(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()