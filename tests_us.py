import unittest 
from datetime import datetime
import Group1
unittest.TestLoader.sortTestMethodsUsing = None


def StringListErrorSearch(prefixStr, idStr, errorList):
    for aString in errorList:
        if aString.startswith(prefixStr) and -1 != aString.find(idStr):
            return True
    return False

# Run test with : 
#  python -m unittest discover -s tests -p 'tests_us.py'
class TestValidationFunctions(unittest.TestCase):
    # US01 Tests
    def test_US01_valid_dates(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I1@)", errors))

    def test_US01_valid_dates_2(self):
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 1990"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I2@)", errors))

    def test_US01_valid_dates_3(self):
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 1980"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I3@)", errors))

    def test_US01_invalid_future_birth_date(self):
        Group1.g_IndiDict["@I4@"] = {"BIRT": "01 JAN 3000"}
        errorsList = Group1.US01Validation()
        self.assertTrue(StringListErrorSearch("Error US01:", "(@I4@)", errorsList))

    def test_US01_invalid_future_death_date(self):
        Group1.g_IndiDict["@I5@"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 3000"}
        errorsList = Group1.US01Validation()
        self.assertTrue(StringListErrorSearch("Error US01:", "(@I5@)", errorsList))

    # US02 Tests
    def test_US02_valid_birth_before_marriage(self):
        Group1.g_IndiDict["@I6@"] = {"BIRT": "01 JAN 1990"}
        Group1.g_IndiDict["@I7@"] = {"BIRT": "01 JAN 1985"}
        Group1.g_FamDict["@F1@"] = {"MARR": "01 JAN 2000", "HUSB": "@I6@", "WIFE": "@I7@"}
        errors = Group1.US02Validation()
        self.assertFalse(StringListErrorSearch("Error US02:", "(@F1@)", errors))

    def test_US02_valid_birth_before_marriage_2(self):
        Group1.g_IndiDict["@I7@"] = {"BIRT": "01 JAN 1985"}
        Group1.g_FamDict["@F2@"] = {"MARR": "01 JAN 1997", "HUSB": "@I6@", "WIFE": "@I7@"}
        errors = Group1.US02Validation()
        self.assertFalse(StringListErrorSearch("Error US02:", "(@F2@)", errors))

    def test_US02_valid_birth_before_marriage_3(self):
        Group1.g_IndiDict["@I8@"] = {"BIRT": "01 JAN 1975"}
        Group1.g_IndiDict["@I9@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_FamDict["@F3@"] = {"MARR": "01 JAN 2005", "HUSB": "@I8@", "WIFE": "@I9@"}
        errors = Group1.US02Validation()
        self.assertFalse(StringListErrorSearch("Error US02:", "(@F3@)", errors))

    def test_US02_invalid_birth_after_marriage(self):
        Group1.g_FamDict["@F4@"] = {"MARR": "01 JAN 1990", "HUSB": "@I8@", "WIFE": "@I9@"}
        errors = Group1.US02Validation()      
        self.assertTrue(StringListErrorSearch("Error US02:", "(@F4@)", errors))

    def test_US02_invalid_birth_same_day_as_marriage(self):
        Group1.g_IndiDict["@I10@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_FamDict["@F5@"] = {"MARR": "01 JAN 2000", "HUSB": "@I8@", "WIFE": "@I9@"}
        errors = Group1.US02Validation()
        self.assertTrue(StringListErrorSearch("Error US02:", "(@F5@)", errors))

    # US03 Tests
    def test_US03_valid_birth_before_death(self):
        Group1.g_IndiDict["I11"] = {"BIRT": "01 JAN 1990", "DEAT": "01 JAN 2000"}
        errors = Group1.US03Validation()
        self.assertFalse(StringListErrorSearch("Error US03:", "(@I11@)", errors))

    def test_US03_valid_birth_before_death_2(self):
        Group1.g_IndiDict["@I12@"] = {"BIRT": "01 JAN 1985", "DEAT": "01 JAN 1990"}
        errors = Group1.US03Validation()
        self.assertFalse(StringListErrorSearch("Error US03:", "(@I12@)", errors))

    def test_US03_valid_birth_before_death_3(self):
        Group1.g_IndiDict["@I13@"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 1980"}
        errors = Group1.US03Validation()
        self.assertFalse(StringListErrorSearch("Error US03:", "(@I13@)", errors))

    def test_US03_invalid_death_before_birth(self):
        Group1.g_IndiDict["@I14@"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 1990"}
        errors = Group1.US03Validation()
        self.assertTrue(StringListErrorSearch("Error US03:", "(@I14@)", errors))

    def test_US03_invalid_death_same_day_as_birth(self):
        Group1.g_IndiDict["@I15@"] = {"BIRT": "01 JAN 2000", "DEAT": "01 JAN 2000"}
        errors = Group1.US03Validation()
        self.assertTrue(StringListErrorSearch("Error US03:", "(@I15@)", errors))

    # US04 Tests
    def test_US04_valid_marriage_before_divorce(self):
        Group1.g_FamDict["@F6@"] = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2010"}
        errors = Group1.US04Validation()
        self.assertFalse(StringListErrorSearch("Error US04:", "(@F6@)", errors))

    def test_US04_valid_marriage_before_divorce_2(self):
        Group1.g_FamDict["@F7@"] = {"MARR": "01 JAN 1990", "DIV": "01 JAN 2000"}
        errors = Group1.US04Validation()
        self.assertFalse(StringListErrorSearch("Error US04:", "(@F7@)", errors))

    def test_US04_valid_marriage_before_divorce_3(self):
        Group1.g_FamDict["@F8@"] = {"MARR": "01 JAN 1980", "DIV": "01 JAN 1990"}
        errors = Group1.US04Validation()
        self.assertFalse(StringListErrorSearch("Error US04:", "(@F8@)", errors))

    def test_US04_invalid_divorce_before_marriage(self):
        Group1.g_FamDict["@F9@"] = {"MARR": "01 JAN 2010", "DIV": "01 JAN 2000"}
        errors = Group1.US04Validation()
        self.assertTrue(StringListErrorSearch("Error US04:", "(@F9@)", errors))

    def test_US04_invalid_divorce_same_day_as_marriage(self):
        Group1.g_FamDict["@F10@"] = {"MARR": "01 JAN 2000", "DIV": "01 JAN 2000"}
        errors = Group1.US04Validation()
        self.assertTrue(StringListErrorSearch("Error US04:", "(@F10@)", errors))

    # US05 Tests
    def test_US05_valid_marriage_before_death(self):
        Group1.g_IndiDict["@I16@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2010"}
        Group1.g_FamDict["@F11@"] = {"MARR": "01 JAN 2000", "HUSB": "@I16@", "WIFE": "@I17@"}
        errors = Group1.US05Validation()
        self.assertFalse(StringListErrorSearch("Error US05:", "(@F11@)", errors))

    def test_US05_valid_marriage_before_death_2(self):
        Group1.g_IndiDict["@I17@"] = {"BIRT": "01 JAN 1975", "DEAT": "01 JAN 2005"}
        Group1.g_FamDict["@F12@"] = {"MARR": "01 JAN 1995", "HUSB": "@I17@", "WIFE": "@I18@"}
        errors = Group1.US05Validation()
        self.assertFalse(StringListErrorSearch("Error US05:", "(@F12@)", errors))

    def test_US05_valid_marriage_before_death_3(self):
        Group1.g_IndiDict["@I18@"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 2000"}
        Group1.g_FamDict["@F13@"] = {"MARR": "01 JAN 1990", "HUSB": "@I18@", "WIFE": "@I19@"}
        errors = Group1.US05Validation()
        self.assertFalse(StringListErrorSearch("Error US05:", "(@F13@)", errors))

    def test_US05_invalid_death_before_marriage(self):
        Group1.g_IndiDict["@I19@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 1990"}
        Group1.g_FamDict["@F14@"] = {"MARR": "01 JAN 2000", "HUSB": "@I19@", "WIFE": "@I20@"}
        errors = Group1.US05Validation()
        self.assertTrue(StringListErrorSearch("Error US05:", "(@F14@)", errors))

    def test_US05_invalid_death_same_day_as_marriage(self):
        Group1.g_IndiDict["@I20@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2000"}
        Group1.g_FamDict["@F15@"] = {"MARR": "01 JAN 2000", "HUSB": "@I20@", "WIFE": "@I21@"}
        errors = Group1.US05Validation()
        self.assertTrue(StringListErrorSearch("Error US05:", "(@F15@)", errors))

    # US06 Tests
    def test_US06_valid_divorce_before_death(self):
        Group1.g_IndiDict["@I21@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2010"}
        Group1.g_FamDict["@F16@"] = {"DIV": "01 JAN 2000", "HUSB": "@I21@", "WIFE": "@I22@"}
        errors = Group1.US06Validation()
        self.assertFalse(StringListErrorSearch("Error US06:", "(@F16@)", errors))

    def test_US06_valid_divorce_before_death_2(self):
        Group1.g_IndiDict["@I22@"] = {"BIRT": "01 JAN 1975", "DEAT": "01 JAN 2005"}
        Group1.g_FamDict["@F17@"] = {"DIV": "01 JAN 1995", "HUSB": "@I22@", "WIFE": "@I23@"}
        errors = Group1.US06Validation()
        self.assertFalse(StringListErrorSearch("Error US06:", "(@F17@)", errors))

    def test_US06_valid_divorce_before_death_3(self):
        Group1.g_IndiDict["@I23@"] = {"BIRT": "01 JAN 1970", "DEAT": "01 JAN 2000"}
        Group1.g_FamDict["@F18@"] = {"DIV": "01 JAN 1990", "HUSB": "@I23@", "WIFE": "@I24@"}
        errors = Group1.US06Validation()
        self.assertFalse(StringListErrorSearch("Error US06:", "(@F18@)", errors))

    def test_US06_invalid_death_before_divorce(self):
        Group1.g_IndiDict["@I24@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 1990"}
        Group1.g_FamDict["@F19@"] = {"DIV": "01 JAN 2000", "HUSB": "@I24@", "WIFE": "@I25@"}
        errors = Group1.US06Validation()
        self.assertTrue(StringListErrorSearch("Error US06:", "(@F19@)", errors))

    def test_US06_invalid_death_same_day_as_divorce(self):
        Group1.g_IndiDict["@I25@"] = {"BIRT": "01 JAN 1980", "DEAT": "01 JAN 2000"}
        Group1.g_FamDict["@F20@"] = {"DIV": "01 JAN 2000", "HUSB": "@I25@", "WIFE": "@I26@"}
        errors = Group1.US06Validation()
        self.assertTrue(StringListErrorSearch("Error US06:", "(@F20@)", errors))

    # US07 Tests
    def test_US07_valid_age_less_than_150_years_deceased(self):
        Group1.g_IndiDict["@I26@"] = {"BIRT": "01 JAN 1900", "DEAT": "01 JAN 2000"}
        errors = Group1.US07Validation()
        self.assertFalse(StringListErrorSearch("Error US07:", "(@I26@)", errors))

    def test_US07_valid_age_less_than_150_years_alive(self):
        Group1.g_IndiDict["@I27@"] = {"BIRT": "01 JAN 1970"}
        errors = Group1.US07Validation()
        self.assertFalse(StringListErrorSearch("Error US07:", "(@I27@)", errors))

    def test_US07_valid_age_less_than_150_years_alive_2(self):
        Group1.g_IndiDict["@I28@"] = {"BIRT": "01 JAN 1900"}
        errors = Group1.US07Validation()
        self.assertFalse(StringListErrorSearch("Error US07:", "(@I28@)", errors))

    def test_US07_invalid_age_more_than_150_years_deceased(self):
        Group1.g_IndiDict["@I29@"] = {"BIRT": "01 JAN 1800", "DEAT": "01 JAN 2000"}
        errors = Group1.US07Validation()
        self.assertTrue(StringListErrorSearch("Error US07:", "(@I29@)", errors))

    def test_US07_invalid_age_more_than_150_years_alive(self):
        Group1.g_IndiDict["@I30@"] = {"BIRT": "01 JAN 1800"}
        errors = Group1.US07Validation()
        self.assertTrue(StringListErrorSearch("Error US07:", "(@I30@)", errors))

    # US08 Tests
    def test_US08_valid_birth_after_marriage(self):
        Group1.g_IndiDict["@I31@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_FamDict["@F21@"] = {"MARR": "01 JAN 1990", "HUSB": "@I32@", "WIFE": "@I33@", "CHIL": "@I31@"}
        errors = Group1.US08Validation()
        self.assertFalse(StringListErrorSearch("Error US08:", "(@I31@)", errors))

    def test_US08_valid_birth_after_marriage_2(self):
        Group1.g_IndiDict["@I34@"] = {"BIRT": "01 JAN 1995"}
        Group1.g_FamDict["@F22@"] = {"MARR": "01 JAN 1980", "HUSB": "@I35@", "WIFE": "@I36@", "CHIL": "@I34@"}
        errors = Group1.US08Validation()
        self.assertFalse(StringListErrorSearch("Error US08:", "(@I34@)", errors))

    def test_US08_valid_birth_after_marriage_3(self):
        Group1.g_IndiDict["@I37@"] = {"BIRT": "01 JAN 1985"}
        Group1.g_FamDict["@F23@"] = {"MARR": "01 JAN 1970", "HUSB": "@I38@", "WIFE": "@I39@", "CHIL": "@I37@"}
        errors = Group1.US08Validation()
        self.assertFalse(StringListErrorSearch("Error US08:", "(@I37@)", errors))

    def test_US08_invalid_birth_before_marriage(self):
        Group1.g_IndiDict["@I40@"] = {"BIRT": "01 JAN 1980"}
        Group1.g_FamDict["@F24@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": "@I40@"}
        errors = Group1.US08Validation()
        self.assertTrue(StringListErrorSearch("Error US08:", "(@I40@)", errors))

    def test_US08_invalid_birth_same_day_as_marriage(self):
        Group1.g_IndiDict["@I43@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_FamDict["@F25@"] = {"MARR": "01 JAN 2000", "HUSB": "@I44@", "WIFE": "@I45@", "CHIL": "@I43@"}
        errors = Group1.US08Validation()
        self.assertTrue(StringListErrorSearch("Error US08:", "(@I43@)", errors))

    # US15 Tests
    def test_US15_01_child(self):
        Group1.g_FamDict["@F99@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": "@I01@"}
        errors = Group1.US15Validation()
        self.assertFalse(StringListErrorSearch("Error US15:", "(@F99@)", errors))  

    def test_US15_10_children(self):
        childStr = ""
        for i in range(10):
            childStr += "@%d@,"
        Group1.g_FamDict["@F99@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": childStr}
        errors = Group1.US15Validation()
        self.assertFalse(StringListErrorSearch("Error US15:", "(@F99@)", errors))  

    def test_US15_14_children(self):
        childStr = ""
        for i in range(14):
            childStr += "@%d@,"
        Group1.g_FamDict["@F99@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": childStr}
        errors = Group1.US15Validation()
        self.assertFalse(StringListErrorSearch("Error US15:", "(@F99@)", errors))  

    def test_US15_15_children(self):
        childStr = ""
        for i in range(15):
            childStr += "@%d@,"
        Group1.g_FamDict["@F99@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": childStr}
        errors = Group1.US15Validation()
        self.assertTrue(StringListErrorSearch("Error US15:", "(@F99@)", errors))  

    def test_US15_20_children(self):
        childStr = ""
        for i in range(20):
            childStr += "@%d@,"
        Group1.g_FamDict["@F99@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": childStr}
        errors = Group1.US15Validation()
        self.assertTrue(StringListErrorSearch("Error US15:", "(@F99@)", errors))  

if __name__ == '__main__':
    unittest.main()
