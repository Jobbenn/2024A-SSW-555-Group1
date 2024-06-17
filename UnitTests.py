from datetime import datetime
import unittest

import Group1

todayStr = datetime.now().strftime('%d %b %Y')

def StringListErrorSearch(prefixStr, idStr, errorList):
    for aString in errorList:
        if aString.startswith(prefixStr) and -1 != aString.find(idStr):
            return True

    return False

class TestUS01Validation(unittest.TestCase):
    def setUp(self):
        Group1.g_IndiDict.clear()

        Group1.g_IndiDict = {'@I1@': {'NAME': 'Tom /Jones/',     'SEX': 'M', 'BIRT': '1 JUL 2003'},         #BIRT good date
              '@I2@': {'NAME': 'Sam /Jones/',     'SEX': 'M', 'BIRT': todayStr},                            #BIRT bad date
              '@I3@': {'NAME': 'Sandra /Hanson/', 'SEX': 'F', 'BIRT': '8 JUL 1970',  'DEAT': '3 MAR 1999'}, #BIRT good date, DEAT good date
              '@I4@': {'NAME': 'Regina /Guster/', 'SEX': 'F', 'BIRT': '5 AUG 1928',  'DEAT': todayStr},     #BIRT good date, DEAT bad date
              '@I5@': {'NAME': 'Ronald /Hanson/', 'SEX': 'M', 'BIRT': todayStr,      'DEAT': todayStr}}     #BIRT bad date, DEAT bad date

    def test_BIRT_good_date(self):
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I1@)", errors))

    def test_BIRT_bad_date(self):
        errors = Group1.US01Validation()
        self.assertTrue(StringListErrorSearch("Error US01:", "(@I2@)", errors))

    def test_DEAT_good_date(self):
        errors = Group1.US01Validation()
        self.assertFalse(StringListErrorSearch("Error US01:", "(@I3@)", errors))

    def test_DEAT_bad_date(self):
        errors = Group1.US01Validation()
        self.assertTrue(StringListErrorSearch("Error US01:", "(@I4@)", errors))

    def test_BIRT_DEAT_bad_date(self):
        errors = Group1.US01Validation()
        self.assertTrue(StringListErrorSearch("Error US01:", "(@I5@)", errors))




if __name__ == '__main__':
    unittest.main()
