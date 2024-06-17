import unittest 
from datetime import datetime
from Group1 import *

# Run test with : 
#  python -m unittest discover -s tests -p 'tests_us.py'
class TestValidationFunctions(unittest.TestCase):
    
    #clear method to ensure a clean state for each test
    def clear(self):
        g_IndiDict.clear()
        g_FamDict.clear()
        
    # US01 Tests
    def test_US01_valid_dates(self):
        g_IndiDict["I1"] = {"BIRT": "01 JAN 2000"}
        US01Validation()
        self.assertEqual(len(g_IndiDict["I1"].get("ERROR", "")), 0)

    def test_US01_valid_dates_2(self):
        g_IndiDict["I2"] = {"BIRT": "01 JAN 1990"}
        US01Validation()
        self.assertEqual(len(g_IndiDict["I2"].get("ERROR", "")), 0)

    def test_US01_valid_dates_3(self):
        g_IndiDict["I3"] = {"BIRT": "01 JAN 1980"}
        US01Validation()
        self.assertEqual(len(g_IndiDict["I3"].get("ERROR", "")), 0)

    def test_US01_invalid_future_birth_date(self):
        g_IndiDict["I4"] = {"BIRT": "01 JAN 3000"}
        US01Validation()
        self.assertIn("US01", g_IndiDict["I4"]["ERROR"])

    def test_US01_invalid_future_death_date(self):
        g_IndiDict["I5"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 3000"}
        US01Validation()
        self.assertIn("US01", g_IndiDict["I5"]["ERROR"])

    # US02 Tests
    def test_US02_valid_birth_before_marriage(self):
        g_IndiDict["I6"] = {"BIRT": "01 JAN 1990"}
        g_FamDict["F1"] = {"MARR": "01 JAN 2000", "HUSB": "I6", "WIFE": "I7"}
        US02Validation()
        self.assertEqual(len(g_FamDict["F1"].get("ERROR", "")), 0)

    def test_US02_valid_birth_before_marriage_2(self):
        g_IndiDict["I7"] = {"BIRT": "01 JAN 1985"}
        g_FamDict["F2"] = {"MARR": "01 JAN 1990", "HUSB": "I6", "WIFE": "I7"}
        US02Validation()
        self.assertEqual(len(g_FamDict["F2"].get("ERROR", "")), 0)

    def test_US02_valid_birth_before_marriage_3(self):
        g_IndiDict["I8"] = {"BIRT": "01 JAN 1975"}
        g_FamDict["F3"] = {"MARR": "01 JAN 1980", "HUSB": "I8", "WIFE": "I9"}
        US02Validation()
        self.assertEqual(len(g_FamDict["F3"].get("ERROR", "")), 0)

    def test_US02_invalid_birth_after_marriage(self):
        g_IndiDict["I9"] = {"BIRT": "01 JAN 2000"}
        g_FamDict["F4"] = {"MARR": "01 JAN 1990", "HUSB": "I8", "WIFE": "I9"}
        US02Validation()
        self.assertIn("US02", g_FamDict["F4"]["ERROR"])

    def test_US02_invalid_birth_same_day_as_marriage(self):
        g_IndiDict["I10"] = {"BIRT": "01 JAN 2000"}
        g_FamDict["F5"] = {"MARR": "01 JAN 2000", "HUSB": "I8", "WIFE": "I9"}
        US02Validation()
        self.assertIn("US02", g_FamDict["F5"]["ERROR"])

    # US03 Tests
    def test_US03_valid_birth_before_death(self):
        g_IndiDict["I11"] = {"BIRT": "01 JAN 1990", "DEAT": "01 JAN 2000"}
        US03Validation()
        self.assertEqual(len(g_IndiDict["I11"].get("ERROR", "")), 0)

    def test_US03_valid_birth_before_death_2(self):
        g_IndiDict["I12"] = {"BIRT": "01 JAN 1985", "DEAT": "01 JAN 1990"}
        US03Validation()
        self.assertEqual(len(g_IndiDict["I12"].get("ERROR", "")), 0)

    def test_US03_valid_birth_before_death_3(self):
        g_IndiDict["I13"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 1980"}
        US03Validation()
        self.assertEqual(len(g_IndiDict["I13"].get("ERROR", "")), 0)

    def test_US03_invalid_death_before_birth(self):
        g_IndiDict["I14"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 1990"}
        US03Validation()
        self.assertIn("US03", g_IndiDict["I14"]["ERROR"])

    def test_US03_invalid_death_same_day_as_birth(self):
        g_IndiDict["I15"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 2000"}
        US03Validation()
        self.assertIn("US03", g_IndiDict["I15"]["ERROR"])

    # US04 Tests
    def test_US04_valid_marriage_before_divorce(self):
        g_FamDict["F6"] = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2010"}
        US04Validation()
        self.assertEqual(len(g_FamDict["F6"].get("ERROR", "")), 0)

    def test_US04_valid_marriage_before_divorce_2(self):
        g_FamDict["F7"] = {"MARR": "01 JAN 1990", "DIV": "01 JAN 2000"}
        US04Validation()
        self.assertEqual(len(g_FamDict["F7"].get("ERROR", "")), 0)

    def test_US04_valid_marriage_before_divorce_3(self):
        g_FamDict["F8"] = {"MARR": "01 JAN 1980", "DIV": "01 JAN 1990"}
        US04Validation()
        self.assertEqual(len(g_FamDict["F8"].get("ERROR", "")), 0)

    def test_US04_invalid_divorce_before_marriage(self):
        g_FamDict["F9"] = {"MARR": "01 JAN 2010", "DIV": "01 JAN 2000"}
        US04Validation()
        self.assertIn("US04", g_FamDict["F9"]["ERROR"])

    def test_US04_invalid_divorce_same_day_as_marriage(self):
        g_FamDict["F10"] = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2000"}
        US04Validation()
        self.assertIn("US04", g_FamDict["F10"]["ERROR"])

    # US05 Tests
    def test_US05_valid_marriage_before_death(self):
        g_IndiDict["I16"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2010"}
        g_FamDict["F11"] = {"MARR": "01 JAN 2000", "HUSB": "I16", "WIFE": "I17"}
        US05Validation()
        self.assertEqual(len(g_FamDict["F11"].get("ERROR", "")), 0)

    def test_US05_valid_marriage_before_death_2(self):
        g_IndiDict["I17"] = {"BIRT": "01 JAN 1975", "DEAT": "01 JAN 2005"}
        g_FamDict["F12"] = {"MARR": "01 JAN 1995", "HUSB": "I17", "WIFE": "I18"}
        US05Validation()
        self.assertEqual(len(g_FamDict["F12"].get("ERROR", "")), 0)

    def test_US05_valid_marriage_before_death_3(self):
        g_IndiDict["I18"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 2000"}
        g_FamDict["F13"] = {"MARR": "01 JAN 1990", "HUSB": "I18", "WIFE": "I19"}
        US05Validation()
        self.assertEqual(len(g_FamDict["F13"].get("ERROR", "")), 0)

    def test_US05_invalid_death_before_marriage(self):
        g_IndiDict["I19"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 1990"}
        g_FamDict["F14"] = {"MARR": "01 JAN 2000", "HUSB": "I19", "WIFE": "I20"}
        US05Validation()
        self.assertIn("US05", g_FamDict["F14"]["ERROR"])

    def test_US05_invalid_death_same_day_as_marriage(self):
        g_IndiDict["I20"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2000"}
        g_FamDict["F15"] = {"MARR": "01 JAN 2000", "HUSB": "I20", "WIFE": "I21"}
        US05Validation()
        self.assertIn("US05", g_FamDict["F15"]["ERROR"])

    # US06 Tests
    def test_US06_valid_divorce_before_death(self):
        g_IndiDict["I21"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2010"}
        g_FamDict["F16"] = {"DIV": "01 JAN 2000", "HUSB": "I21", "WIFE": "I22"}
        US06Validation()
        self.assertEqual(len(g_FamDict["F16"].get("ERROR", "")), 0)

    def test_US06_valid_divorce_before_death_2(self):
        g_IndiDict["I22"] = {"BIRT": "01 JAN 1975", "DEAT": "01 JAN 2005"}
        g_FamDict["F17"] = {"DIV": "01 JAN 1995", "HUSB": "I22", "WIFE": "I23"}
        US06Validation()
        self.assertEqual(len(g_FamDict["F17"].get("ERROR", "")), 0)

    def test_US06_valid_divorce_before_death_3(self):
        g_IndiDict["I23"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 2000"}
        g_FamDict["F18"] = {"DIV": "01 JAN 1990", "HUSB": "I23", "WIFE": "I24"}
        US06Validation()
        self.assertEqual(len(g_FamDict["F18"].get("ERROR", "")), 0)

    def test_US06_invalid_death_before_divorce(self):
        g_IndiDict["I24"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 1990"}
        g_FamDict["F19"] = {"DIV": "01 JAN 2000", "HUSB": "I24", "WIFE": "I25"}
        US06Validation()
        self.assertIn("US06", g_FamDict["F19"]["ERROR"])

    def test_US06_invalid_death_same_day_as_divorce(self):
        g_IndiDict["I25"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2000"}
        g_FamDict["F20"] = {"DIV": "01 JAN 2000", "HUSB": "I25", "WIFE": "I26"}
        US06Validation()
        self.assertIn("US06", g_FamDict["F20"]["ERROR"])

    # US07 Tests
    def test_US07_valid_age_less_than_150_years_deceased(self):
        g_IndiDict["I26"] = {"BIRT": "01 JAN 1900", "DEAT": "01 JAN 2000"}
        US07Validation()
        self.assertEqual(len(g_IndiDict["I26"].get("ERROR", "")), 0)

    def test_US07_valid_age_less_than_150_years_alive(self):
        g_IndiDict["I27"] = {"BIRT": "01 JAN 1970"}
        US07Validation()
        self.assertEqual(len(g_IndiDict["I27"].get("ERROR", "")), 0)

    def test_US07_valid_age_less_than_150_years_alive_2(self):
        g_IndiDict["I28"] = {"BIRT": "01 JAN 1900"}
        US07Validation()
        self.assertEqual(len(g_IndiDict["I28"].get("ERROR", "")), 0)

    def test_US07_invalid_age_more_than_150_years_deceased(self):
        g_IndiDict["I29"] = {"BIRT": "01 JAN 1800", "DEAT": "01 JAN 2000"}
        US07Validation()
        self.assertIn("US07", g_IndiDict["I29"]["ERROR"])

    def test_US07_invalid_age_more_than_150_years_alive(self):
        g_IndiDict["I30"] = {"BIRT": "01 JAN 1800"}
        US07Validation()
        self.assertIn("US07", g_IndiDict["I30"]["ERROR"])

    # US08 Tests
    def test_US08_valid_birth_after_marriage(self):
        g_IndiDict["I31"] = {"BIRT": "01 JAN 2000"}
        g_FamDict["F21"] = {"MARR": "01 JAN 1990", "HUSB": "I32", "WIFE": "I33", "CHIL": "I31"}
        US08Validation()
        self.assertEqual(len(g_IndiDict["I31"].get("ERROR", "")), 0)

    def test_US08_valid_birth_after_marriage_2(self):
        g_IndiDict["I34"] = {"BIRT": "01 JAN 1995"}
        g_FamDict["F22"] = {"MARR": "01 JAN 1980", "HUSB": "I35", "WIFE": "I36", "CHIL": "I34"}
        US08Validation()
        self.assertEqual(len(g_IndiDict["I34"].get("ERROR", "")), 0)

    def test_US08_valid_birth_after_marriage_3(self):
        g_IndiDict["I37"] = {"BIRT": "01 JAN 1985"}
        g_FamDict["F23"] = {"MARR": "01 JAN 1970", "HUSB": "I38", "WIFE": "I39", "CHIL": "I37"}
        US08Validation()
        self.assertEqual(len(g_IndiDict["I37"].get("ERROR", "")), 0)

    def test_US08_invalid_birth_before_marriage(self):
        g_IndiDict["I40"] = {"BIRT": "01 JAN 1980"}
        g_FamDict["F24"] = {"MARR": "01 JAN 1990", "HUSB": "I41", "WIFE": "I42", "CHIL": "I40"}
        US08Validation()
        self.assertIn("US08", g_IndiDict["I40"]["ERROR"])

    def test_US08_invalid_birth_same_day_as_marriage(self):
        g_IndiDict["I43"] = {"BIRT": "01 JAN 2000"}
        g_FamDict["F25"] = {"MARR": "01 JAN 2000", "HUSB": "I44", "WIFE": "I45", "CHIL": "I43"}
        US08Validation()
        self.assertIn("US08", g_IndiDict["I43"]["ERROR"])

if __name__ == '__main__':
    unittest.main()