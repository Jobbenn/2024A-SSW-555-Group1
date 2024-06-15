import unittest
from datetime import datetime
from Group1 import US04Validation, g_FamDict, AppendDictStr

class TestUS04Validation(unittest.TestCase):

    def setUp(self):
        # Setting up test data
        self.famDict1 = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2010"}  # Should pass
        self.famDict2 = {"MARR": "01 JAN 2010", "DIV": "01 JAN 2000"}  # Should fail
        self.famDict3 = {"MARR": "01 JAN 2000"}                        # Should pass
        self.famDict4 = {"DIV": "01 JAN 2010"}                         # Should pass
        self.famDict5 = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2000"}  # Should pass

    def test_marriage_before_divorce(self):
        g_FamDict["F1"] = self.famDict1
        US04Validation()
        self.assertNotIn("ERROR", g_FamDict["F1"])

    def test_divorce_before_marriage(self):
        g_FamDict["F2"] = self.famDict2
        US04Validation()
        self.assertIn("ERROR", g_FamDict["F2"])
        self.assertIn("US04", g_FamDict["F2"]["ERROR"])

    def test_marriage_without_divorce(self):
        g_FamDict["F3"] = self.famDict3
        US04Validation()
        self.assertNotIn("ERROR", g_FamDict["F3"])

    def test_divorce_without_marriage(self):
        g_FamDict["F4"] = self.famDict4
        US04Validation()
        self.assertNotIn("ERROR", g_FamDict["F4"])

    def test_marriage_and_divorce_on_same_day(self):
        g_FamDict["F5"] = self.famDict5
        US04Validation()
        self.assertNotIn("ERROR", g_FamDict["F5"])

if __name__ == '__main__':
    unittest.main()