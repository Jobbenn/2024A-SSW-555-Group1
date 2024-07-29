import unittest 
from datetime import datetime, timedelta
import Group1
unittest.TestLoader.sortTestMethodsUsing = None

class TestValidationFunctions(unittest.TestCase):
    def setUp(self):
        Group1.g_IndiDict.clear()
        Group1.g_FamDict.clear()

def StringListErrorSearch(prefixStr, idStr, errorList):
    for aString in errorList:
        if aString.startswith(prefixStr) and -1 != aString.find(idStr):
            return True
    return False

def StringListErrorStarts(errorStr, errorList):
    for aString in errorList:
        if aString.startswith(errorStr):
            return True
    return False

class TestValidationFunctions(unittest.TestCase):
    # US01 Tests
    def test_US01_valid_dates(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000", "SEX":"M"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I1@)", errors))

    def test_US01_valid_dates_2(self):
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 1990", "SEX":"F"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I2@)", errors))

    def test_US01_valid_dates_3(self):
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 1980", "SEX":"M"}
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I3@)", errors))

    def test_US01_invalid_future_birth_date(self):
        Group1.g_IndiDict["@I4@"] = {"BIRT": "01 JAN 3000", "SEX":"F"}
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
        self.assertTrue(StringListErrorSearch("Error US05:", "(@I20@)", errors))

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
        self.assertTrue(StringListErrorSearch("Error US06:", "(@I25@)", errors))

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
        Group1.g_IndiDict["@I40@"] = {"BIRT": "01 JAN 1980", "NAME": "Child"}
        Group1.g_FamDict["@F24@"] = {"MARR": "01 JAN 1990", "HUSB": "@I41@", "WIFE": "@I42@", "CHIL": ["@I40@"]}
        errors = Group1.US08Validation()
        self.assertTrue(StringListErrorSearch("Error US08:", "(@I40@)", errors))

    def test_US08_invalid_birth_same_day_as_marriage(self):
        Group1.g_IndiDict["@I43@"] = {"BIRT": "01 JAN 2000", "NAME": "Child"}
        Group1.g_FamDict["@F30@"] = {"MARR": "01 JAN 2000", "HUSB": "@I16@", "WIFE": "@I17@", "CHIL": ["@I43@"]}
        errors = Group1.US08Validation()
        self.assertTrue(StringListErrorSearch("Error US08:", "(@I43@)", errors))

    #US09 Tests
    def test_US09_child_after_father_death(self):
        Group1.g_IndiDict["@I31@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_FamDict["@F21@"] = {"MARR": "01 JAN 1990", "HUSB": "@I32@", "WIFE": "@I33@", "CHIL": "@I31@"}
        errors = Group1.US09Validation()
        self.assertFalse(StringListErrorSearch("Error US09:", "(@I31@)", errors))

    def test_US09_child_before_parents_death(self):
        Group1.g_IndiDict["@I34@"] = {"BIRT": "01 JAN 1995"}
        Group1.g_FamDict["@F22@"] = {"MARR": "01 JAN 1980", "HUSB": "@I35@", "WIFE": "@I36@", "CHIL": "@I34@"}
        errors = Group1.US09Validation()
        self.assertFalse(StringListErrorSearch("Error US09:", "(@I34@)", errors))

    def test_US09_child_more_than_9_months_after_father_death(self):
        Group1.g_IndiDict["@I43@"] = {"BIRT": "01 JAN 2000", "NAME": "Child"}
        Group1.g_FamDict["@F30@"] = {"MARR": "01 JAN 2000", "HUSB": "@I16@", "WIFE": "@I17@", "CHIL": ["@I43@"]}
        errors = Group1.US09Validation()
        self.assertFalse(StringListErrorSearch("Error US09:", "(@I43@)", errors))
        

    # US10 Tests
    def test_US_10_husband_under_14(self):
        Group1.g_IndiDict["@I9@"] = {"BIRT": "01 JAN 2010", "NAME": "Mr. Husband"}
        Group1.g_IndiDict["@I11@"] = {"BIRT": "01 JAN 2000", "NAME": "Ms. Wife"}
        Group1.g_FamDict["@F24@"] = {"MARR": "04 JAN 2015", "HUSB": "@I9@", "WIFE": "@I11@", "CHIL": ["@I40@"]}
        errors = Group1.US10Validation()
        self.assertTrue(StringListErrorSearch("Anomaly US10:", "(@I9@)", errors))
    
    def test_US_10_wife_under_14(self):
        Group1.g_IndiDict["I9"] = {"BIRT": "01 JAN 2000", "NAME": "Mr. Husband"}
        Group1.g_IndiDict["I11"] = {"BIRT": "01 JAN 2008", "NAME": "Ms. Wife"}
        Group1.g_FamDict["F24"] = {"MARR": "04 JAN 2015", "HUSB": "I9", "WIFE": "I11", "CHIL": ["@I40@"]}
        errors = Group1.US10Validation()
        self.assertTrue(StringListErrorSearch("Anomaly US10:", "(I11)", errors))

    # US12 Tests
    def test_US12_valid_parent_age_difference(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 1950", "SEX": "M"}
        Group1.g_IndiDict["@I2@"] = {"BIRT": "05 MAY 1955", "SEX": "F"}
        Group1.g_IndiDict["@I3@"] = {"BIRT": "15 MAR 1975"}
        Group1.g_IndiDict["@I4@"] = {"BIRT": "10 DEC 1980"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "CHIL": ["@I3@", "@I4@"]}
        errors = Group1.US12Validation()
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I3@)", errors))
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I4@)", errors))

    def test_US12_valid_parent_age_difference_2(self):
        Group1.g_IndiDict["@I5@"] = {"BIRT": "01 JAN 1940", "SEX": "M"}
        Group1.g_IndiDict["@I6@"] = {"BIRT": "05 MAY 1950", "SEX": "F"}
        Group1.g_IndiDict["@I7@"] = {"BIRT": "15 MAR 1965"}
        Group1.g_IndiDict["@I8@"] = {"BIRT": "10 DEC 1970"}
        Group1.g_FamDict["@F2@"] = {"HUSB": "@I5@", "WIFE": "@I6@", "CHIL": ["@I7@", "@I8@"]}
        errors = Group1.US12Validation()
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I7@)", errors))
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I8@)", errors))

    def test_US12_valid_parent_age_difference_3(self):
        Group1.g_IndiDict["@I9@"] = {"BIRT": "01 JAN 1960", "SEX": "M"}
        Group1.g_IndiDict["@I10@"] = {"BIRT": "05 MAY 1965", "SEX": "F"}
        Group1.g_IndiDict["@I11@"] = {"BIRT": "15 MAR 1990"}
        Group1.g_IndiDict["@I12@"] = {"BIRT": "10 DEC 1995"}
        Group1.g_FamDict["@F3@"] = {"HUSB": "@I9@", "WIFE": "@I10@", "CHIL": ["@I11@", "@I12@"]}
        errors = Group1.US12Validation()
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I11@)", errors))
        self.assertFalse(StringListErrorSearch("Error US12:", "(@I12@)", errors))

    def test_US12_invalid_mother_age_difference(self):
        Group1.g_IndiDict["@I13@"] = {"BIRT": "20 JUN 1920", "SEX": "F"}  
        Group1.g_IndiDict["@I14@"] = {"BIRT": "22 APR 1985"}
        Group1.g_FamDict["@F4@"] = {"HUSB": "@I9@", "WIFE": "@I13@", "CHIL": ["@I14@"]}
        errors = Group1.US12Validation()
        self.assertTrue(StringListErrorSearch("Error US12:", "(@I14@)", errors))

    def test_US12_invalid_father_age_difference(self):
        Group1.g_IndiDict["@I15@"] = {"BIRT": "01 JAN 1900", "SEX": "M"}  
        Group1.g_IndiDict["@I16@"] = {"BIRT": "20 JUN 1960", "SEX": "F"}
        Group1.g_IndiDict["@I17@"] = {"BIRT": "22 APR 1985"}
        Group1.g_FamDict["@F5@"] = {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I17@"]}
        errors = Group1.US12Validation()
        self.assertTrue(StringListErrorSearch("Error US12:", "(@I17@)", errors))
        
    # US13 Tests
    def test_US13_valid_sibling_birth_dates(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 SEP 2000"}
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_FamDict["@F1@"] = {"CHIL": ["@I1@", "@I2@", "@I3@"]}
        errors = Group1.US13Validation()
        self.assertFalse(StringListErrorSearch("Error US13:", "@F1@", errors))
    
    def test_US13_valid_sibling_birth_dates_twins(self):
        Group1.g_IndiDict["@I7@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I8@"] = {"BIRT": "02 JAN 2000"}
        Group1.g_FamDict["@F3@"] = {"CHIL": ["@I7@", "@I8@"]}
        errors = Group1.US13Validation()
        self.assertFalse(StringListErrorSearch("Error US13:", "@F3@", errors))

    def test_US13_invalid_sibling_birth_dates(self):
        Group1.g_IndiDict["@I7@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I8@"] = {"BIRT": "02 JAN 2000"}
        Group1.g_FamDict["@F3@"] = {"CHIL": ["@I7@", "@I8@"]}
        errors = Group1.US13Validation()
        self.assertFalse(StringListErrorSearch("Error US13:", "@F3@", errors))
        
    def test_US13_valid_sibling_birth_dates_more_than_8_months(self):
        Group1.g_IndiDict["@I8@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I9@"] = {"BIRT": "01 OCT 2000"}
        Group1.g_FamDict["@F4@"] = {"CHIL": ["@I8@", "@I9@"]}
        errors = Group1.US13Validation()
        self.assertFalse(StringListErrorSearch("Error US13:", "@F4@", errors))

    def test_US13_invalid_sibling_birth_dates_within_8_months(self):
        Group1.g_IndiDict["@I10@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I11@"] = {"BIRT": "01 JUL 2000"}
        Group1.g_FamDict["@F5@"] = {"CHIL": ["@I10@", "@I11@"]}
        errors = Group1.US13Validation()
        self.assertTrue(StringListErrorSearch("Error US13:", "@F5@", errors))
    
    # US14 Tests
    def test_US14_5_siblings_same_birth(self):
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I4@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I5@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I6@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I7@"] = {"BIRT": "02 MAR 2007"}
        Group1.g_FamDict["@F1@"] = {"CHIL": ["@I2@", "@I3@", "@I4@", "@I5@", "@I6@", "@I7@"]}
        errors = Group1.US14Validation()
        self.assertTrue(StringListErrorSearch("Anomaly US14:", "F1", errors))
    
    def test_US14_5_siblings_same_birth_false(self):
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I4@"] = {"BIRT": "01 JAN 2003"}
        Group1.g_IndiDict["@I5@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I6@"] = {"BIRT": "01 JAN 2002"}
        Group1.g_IndiDict["@I7@"] = {"BIRT": "02 MAR 2007"}
        Group1.g_FamDict["@F1@"] = {"CHIL": ["@I2@", "@I3@", "@I4@", "@I5@", "@I6@", "@I7@"]}
        errors = Group1.US14Validation()
        self.assertFalse(StringListErrorSearch("Anomaly US14:", "F1", errors))

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

    # US21 Tests
    def test_US21_Gender_HMWF(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000", "SEX":"M"}
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 2000", "SEX":"F"}
        Group1.g_FamDict["@F99@"] = {"HUSB": "@I1@", "WIFE": "@I2@"}
        errors = Group1.US21Validation()
        self.assertTrue(StringListErrorSearch("Error US21:", "(@F99@)", errors))
        
    def test_US21_Gender_HFWF(self):
        Group1.g_IndiDict["@I2@"] = {"BIRT": "01 JAN 2000", "SEX":"F"}
        Group1.g_IndiDict["@I4@"] = {"BIRT": "01 JAN 2000", "SEX":"F"}
        Group1.g_FamDict["@F99@"] = {"HUSB": "@I2@", "WIFE": "@I4@"}
        errors = Group1.US21Validation()
        self.assertTrue(StringListErrorSearch("Error US21:", "(@F99@)", errors))

    def test_US21_Gender_HMWM(self):
        Group1.g_FamDict["@F99@"] = {"HUSB": "@I1@", "WIFE": "@I3@"}
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000", "SEX":"M"}
        Group1.g_IndiDict["@I3@"] = {"BIRT": "01 JAN 2000", "SEX":"M"}
        errors = Group1.US21Validation()
        self.assertTrue(StringListErrorSearch("Error US21:", "(@F99@)", errors))

    # US22 Tests
    def test_US22_Good(self):
        del Group1.g_IndiDict["@F99@"]
        errors = Group1.US22Validation()
        self.assertFalse(StringListErrorStarts("Error US22:", errors))

    def test_US22_Bad(self):
        Group1.g_IndiDict["@F99@"] = {"BIRT": "01 JAN 2000", "SEX":"M"}
        errors = Group1.US22Validation()
        self.assertTrue(StringListErrorStarts("Error US22:", errors))

    # US24 Tests
    def test_US24_Duplicates(self):
        Group1.g_FamDict["@F88@"] = {"MARR": "04 MAY 1994", "HUSB": "@I1@", "WIFE": "@I3@"}
        Group1.g_FamDict["@F89@"] = {"MARR": "04 MAY 1991", "HUSB": "@I1@", "WIFE": "@I3@"}
        Group1.g_FamDict["@F90@"] = {"MARR": "04 MAY 1994", "HUSB": "@I1@", "WIFE": "@I3@"}
        errors = Group1.US24Validation()
        self.assertTrue(StringListErrorSearch("Error US24:", "04 MAY 1994", errors))
    
    def test_US24_No_Duplicates(self):
        Group1.g_FamDict["@F91@"] = {"MARR": "04 MAY 1997", "HUSB": "@I1@", "WIFE": "@I3@"}
        Group1.g_FamDict["@F92@"] = {"MARR": "04 MAY 1998", "HUSB": "@I1@", "WIFE": "@I3@"}
        errors = Group1.US24Validation()
        self.assertFalse(StringListErrorSearch("Error US24:", "04 MAY 1997", errors))
    
    # US26 Tests
    def test_US26_FAMC_No_CHIL(self):
        Group1.g_IndiDict["@I53@"] = {"BIRT": "01 JAN 2000", "SEX":"M", "FAMC": "@F93@"}
        Group1.g_FamDict["@F93@"] = {"MARR": "04 MAY 1994", "HUSB": "@I1@", "WIFE": "@I3@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertTrue(StringListErrorSearch("Error US26:", "@I53@", errors))
    
    def test_US26_FAMC_No_Spouse(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        
        Group1.g_IndiDict["@I53@"] = {"BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F93@"}
        Group1.g_FamDict["@F93@"] = {"MARR": "04 MAY 1994", "HUSB": "@I1@", "WIFE": "@I2@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertTrue(StringListErrorSearch("Error US26:", "@I53@", errors))
    
    def test_US26_FAMC_Yes_Spouse(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_FamDict["@F94@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertFalse(StringListErrorSearch("Error US26:", "@I54@", errors))
    
    def test_US26_HUSB_No_FAMS(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        
        Group1.g_IndiDict = {}
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F77@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F94@"}
        Group1.g_FamDict["@F94@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertTrue(StringListErrorSearch("Error US26:", "@F94@", errors))
    
    def test_US26_HUSB_Yes_FAMS(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        
        Group1.g_IndiDict = {}
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F94@"}
        Group1.g_FamDict["@F94@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertFalse(StringListErrorSearch("Error US26:", "@F94@", errors))
    
    def test_US26_WIFE_No_FAMS(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        
        Group1.g_IndiDict = {}
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F77@"}
        Group1.g_FamDict["@F94@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertTrue(StringListErrorSearch("Error US26:", "@F94@", errors))
    
    def test_US26_WIFE_Yes_FAMS(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}

        Group1.g_IndiDict = {}
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F94@"}
        Group1.g_FamDict["@F94@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": []}
        errors = Group1.US26Validation()
        self.assertFalse(StringListErrorSearch("Error US26:", "@F94@", errors))
    
    #test for chil no fams
    def test_US26_CHIL_No_FAMC(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        #parents
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F77@"}
        #children
        Group1.g_IndiDict["@I57@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMC": "@F01@"}
        #fam
        Group1.g_FamDict["@F95@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": ['@I57@']}
        errors = Group1.US26Validation()
        self.assertTrue(StringListErrorSearch("Error US26:", "@I57@", errors))
    
    def test_US26_CHIL_Yes_FAMC(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}
        #parents
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMS": "@F77@"}
        #children
        Group1.g_IndiDict["@I57@"] = {"NAME": "Sallie Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMC": "@F95@"}
        Group1.g_IndiDict["@I58@"] = {"NAME": "Jenn Barker", "BIRT": "01 JAN 2000", "SEX":"F", "FAMC": "@F95@"}
        #fam
        Group1.g_FamDict["@F95@"] = {"MARR": "04 MAY 1994", "HUSB": "@I54@", "WIFE": "@I55@", "CHIL": ['@I57@', '@I58@']}
        errors = Group1.US26Validation()
        self.assertFalse(StringListErrorSearch("Error US26:", "@I57@", errors))

    # US31 Tests
    def test_US31_living_single(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "John Doe", "BIRT": "01 JAN 1980", "SEX": "M"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Jane Smith", "BIRT": "01 FEB 1985", "SEX": "F", "DEAT": "01 JAN 2020"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Alice Doe", "BIRT": "01 JAN 2010", "SEX": "F"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Bob Doe", "BIRT": "01 JAN 1985", "SEX": "M"}
        Group1.g_IndiDict["@I5@"] = {"NAME": "Carol Smith", "BIRT": "01 FEB 1987", "SEX": "F"}
        Group1.g_IndiDict["@I6@"] = {"NAME": "Daisy Jones", "BIRT": "01 MAR 1990", "SEX": "F"}
        Group1.g_IndiDict["@I7@"] = {"NAME": "Eve Johnson", "BIRT": "01 APR 1992", "SEX": "F", "FAMS": "@F2@"}

        expected = ["John Doe", "Alice Doe", "Bob Doe", "Carol Smith", "Daisy Jones"]
        result = Group1.List_US31()
        self.assertEqual(sorted(result), sorted(expected))

    #US33 Tests
    def test_US33_orphans(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Father", "DEAT": "01 JAN 2010"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Mother", "DEAT": "01 JAN 2011"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Child 1", "BIRT": "01 JAN 2005"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Child 2", "BIRT": "01 JAN 2010"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "CHIL": ["@I3@", "@I4@"]}

        expected = ['@I3@', '@I4@']
        result = Group1.List_US33()
        self.assertEqual(result, expected)

    def test_US33_no_orphans(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Father", "DEAT": "01 JAN 2010"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Mother", "DEAT": "01 JAN 2011"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Child 1", "BIRT": "01 JAN 1990"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Child 2", "BIRT": "01 JAN 1985"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "CHIL": ["@I3@", "@I4@"]}

        expected = []
        result = Group1.List_US33()
        self.assertEqual(result, expected)

    # US34 Tests
    def test_US34_large_age_difference(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Husband", "BIRT": "01 JAN 1950"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Wife", "BIRT": "01 JAN 1980"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Husband", "BIRT": "01 JAN 1960"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Wife", "BIRT": "01 JAN 1970"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "MARR": "01 JAN 2000"}
        Group1.g_FamDict["@F2@"] = {"HUSB": "@I3@", "WIFE": "@I4@", "MARR": "01 JAN 2000"}

        expected = ['@F1@']
        result = Group1.List_US34()
        self.assertEqual(result, expected)

    def test_US34_no_large_age_difference(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Husband", "BIRT": "01 JAN 1960"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Wife", "BIRT": "01 JAN 1970"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Husband", "BIRT": "01 JAN 1965"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Wife", "BIRT": "01 JAN 1975"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "MARR": "01 JAN 2000"}
        Group1.g_FamDict["@F2@"] = {"HUSB": "@I3@", "WIFE": "@I4@", "MARR": "01 JAN 2000"}

        expected = []
        result = Group1.List_US34()
        self.assertEqual(result, expected)
        
    # US32 Tests
    def test_US32_multiple_births(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Alice", "BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Bob", "BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Charlie", "BIRT": "01 FEB 2000"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "David", "BIRT": "01 FEB 2000"}
        Group1.g_IndiDict["@I5@"] = {"NAME": "Eve", "BIRT": "01 MAR 2000"}
        Group1.g_FamDict["@F1@"] = {"CHIL": ["@I1@", "@I2@", "@I3@", "@I4@", "@I5@"]}

        expected = {'@F1@': [('01 JAN 2000', ['@I1@', '@I2@']), ('01 FEB 2000', ['@I3@', '@I4@'])]}
        result = Group1.List_US32()
        self.assertEqual(result, expected)

    def test_US32_no_multiple_births(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "Alice", "BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Bob", "BIRT": "01 JAN 2001"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Charlie", "BIRT": "01 FEB 2002"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "David", "BIRT": "01 FEB 2003"}
        Group1.g_IndiDict["@I5@"] = {"NAME": "Eve", "BIRT": "01 MAR 2004"}
        Group1.g_FamDict["@F1@"] = {"CHIL": ["@I1@", "@I2@", "@I3@", "@I4@", "@I5@"]}

        expected = {}
        result = Group1.List_US32()
        self.assertEqual(result, expected)

    # US38 Test
    def test_US38(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}

        Group1.g_IndiDict = {}
        Group1.g_IndiDict["@I54@"] = {"NAME": "Bob Barker", "BIRT": "19 AUG 2000", "SEX":"M", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I55@"] = {"NAME": "Sally Barker", "BIRT": "24 AUG 2000", "SEX":"F", "FAMS": "@F94@"}
        Group1.g_IndiDict["@I56@"] = {"NAME": "Falsetto Barker", "BIRT": "25 DEC 2000", "SEX":"F", "FAMS": "@F94@"}
        upcoming = Group1.List_US38()
        self.assertEqual(upcoming, ['Individual @I54@: Bob Barker', 'Individual @I55@: Sally Barker'])
    
    # US39 Test
    def test_US39(self):
        #reset
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}

        #FAM_positive
        Group1.g_IndiDict["@I1@"] = {"NAME": "Bob Barker", "BIRT": "01 JAN 2000", "SEX":"M"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Sally Barker", "BIRT": "01 JAN 2000", "SEX":"F"}
        Group1.g_FamDict["@F1@"] = {"MARR": "24 AUG 1994", "HUSB": "@I1@", "WIFE": "@I2@"}

        #FAM_negative
        Group1.g_IndiDict["@I3@"] = {"NAME": "Lucy Lemming", "BIRT": "01 JAN 2000", "SEX":"F"}
        Group1.g_IndiDict["@I4@"] = {"NAME": "Larry Lemming", "BIRT": "01 JAN 2000", "SEX":"M"}
        Group1.g_FamDict["@F2@"] = {"MARR": "04 MAY 1994", "HUSB": "@I4@", "WIFE": "@I3@"}

        upcoming = Group1.List_US39()
        self.assertEqual(upcoming, ['Family @F1@: Bob Barker and Sally Barker'])

# US37 Tests
    def test_US37_recent_survivors(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "John Doe", "DEAT": (datetime.today() - timedelta(days=5)).strftime("%d %b %Y"), "FAMS": "@F1@"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Jane Doe", "FAMS": "@F1@"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Baby Doe"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "CHIL": ["@I3@"]}

        expected = ["Jane Doe", "Baby Doe"]
        result = Group1.List_US37()
        self.assertEqual(result, expected)

    def test_US37_no_recent_deaths(self):
        Group1.g_IndiDict["@I1@"] = {"NAME": "John Doe", "DEAT": (datetime.today() - timedelta(days=50)).strftime("%d %b %Y"), "FAMS": "@F1@"}
        Group1.g_IndiDict["@I2@"] = {"NAME": "Jane Doe", "FAMS": "@F1@"}
        Group1.g_IndiDict["@I3@"] = {"NAME": "Baby Doe"}
        Group1.g_FamDict["@F1@"] = {"HUSB": "@I1@", "WIFE": "@I2@", "CHIL": ["@I3@"]}

        expected = []
        result = Group1.List_US37()
        self.assertEqual(result, expected)

# US42 tests
    def test_US42(self):
        Group1.g_IndiDict = {}
        Group1.g_FamDict = {}

    def test_US42_invalid_death_date(self):
        Group1.g_IndiDict["@I2@"] = {"DEAT": "31 FEB 2020"}  # Invalid date
        expected = ["Error US42: Individual @I2@ has an invalid death date."]
        result = Group1.List_US42()
        self.assertEqual(result, expected)

    def test_US42_no_invalid_dates(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"DEAT": "01 FEB 2020"}
        Group1.g_FamDict["@F1@"] = {"MARR": "01 JAN 1990"}
        Group1.g_FamDict["@F2@"] = {"DIV": "01 JUN 2000"}
        expected = []
        result = Group1.List_US42()
        self.assertEqual(result, expected)

#35 & 36
    def test_US35(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"DEAT": "01 FEB 2020"}
        Group1.g_FamDict["@F1@"] = {"MARR": "01 JAN 1990"}
        Group1.g_FamDict["@F2@"] = {"DIV": "01 JUN 2000"}
        expected = []
        result = Group1.List_US35()
        self.assertEqual(result, expected)

    def test_US36(self):
        Group1.g_IndiDict["@I1@"] = {"BIRT": "01 JAN 2000"}
        Group1.g_IndiDict["@I2@"] = {"DEAT": "01 FEB 2020"}
        Group1.g_FamDict["@F1@"] = {"MARR": "01 JAN 1990"}
        Group1.g_FamDict["@F2@"] = {"DIV": "01 JUN 2000"}
        expected = []
        result = Group1.List_US36()
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
