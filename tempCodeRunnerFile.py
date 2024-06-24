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
