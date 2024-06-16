import unittest
from datetime import datetime
from Group1 import US07Validation, US08Validation

class TestGEDCOMFunctions(unittest.TestCase):

    # US07 Tests
    def test_US07_less_than_150_years_old_deceased(self):
        self.assertTrue(US07Validation("01 JAN 1900", "01 JAN 2000"))

    def test_US07_less_than_150_years_old_alive(self):
        self.assertTrue(US07Validation("01 JAN 1900"))

    

    # US08 Tests
    def test_US08_birth_before_marriage(self):
        self.assertFalse(US08Validation("01 JAN 1990", "01 JAN 2000"))

    def test_US08_birth_after_marriage(self):
        self.assertTrue(US08Validation("01 JAN 2000", "01 JAN 1999"))

    def test_US08_birth_long_after_marriage(self):
        self.assertTrue(US08Validation("01 JAN 2000", "01 JAN 1980"))

    
if __name__ == '__main__':
    unittest.main()
