#Group 1 Program

from prettytable import PrettyTable
from datetime import datetime, timedelta
from collections import defaultdict

#-------------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------------

g_IndividualsTable = PrettyTable()
g_FamiliesTable = PrettyTable()

g_IndiDict = {}
g_FamDict = {}

lstValidTags = ["INDI",
                "NAME",
                "SEX",
                "BIRT",
                "DEAT",
                "FAMC",
                "FAMS",
                "FAM",
                "MARR",
                "HUSB",
                "WIFE",
                "CHIL",
                "DIV",
                "DATE",
                "HEAD",
                "TRLR",
                "NOTE"]

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Utility Functions
#-------------------------------------------------------------------------------

def AgeDateTimeCalc(startDT, endDT):
    durationDT = endDT - startDT
    ageYears = durationDT.days / 365.2425
    return int(ageYears)

def AppendDictStr(key, dictItem, appendStr, spacerStr):
    if key in dictItem:
        oldValueStr = dictItem[key]
        dictItem[key] = oldValueStr + spacerStr+ appendStr
    else:
        dictItem[key] = appendStr

def calculate_age(birth_date, death_date=None):
    birth_dt = datetime.strptime(birth_date, "%d %b %Y")
    if death_date:
        end_dt = datetime.strptime(death_date, "%d %b %Y")
    else:
        end_dt = datetime.today()
    return AgeDateTimeCalc(birth_dt, end_dt)

def calculate_days(date):
    theDate = datetime.strptime(date, "%d %b %Y")

    durationDate = datetime.today() - theDate

    return durationDate.days

def get_individual_birth_date(individual_id):
    if individual_id in g_IndiDict and "BIRT" in g_IndiDict[individual_id]:
        return datetime.strptime(g_IndiDict[individual_id]["BIRT"], "%d %b %Y")
    return None

def validate_parent_child_age_difference(parent_id, child_birth_date, max_age_difference):
    parent_birth_date = get_individual_birth_date(parent_id)
    if parent_birth_date:
        age_at_birth = (child_birth_date - parent_birth_date).days / 365.25
        return age_at_birth < max_age_difference
    return True

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Data Validation Functions
#-------------------------------------------------------------------------------

#User Story 01 Dates before current date
def US01Validation():
    errors = []

    today = datetime.today()

    for anIndi in g_IndiDict.keys():
        valid = True

        birthDT = datetime.strptime(g_IndiDict[anIndi]["BIRT"], "%d %b %Y")

        if birthDT >= today:
            valid = False
        
        if "DEAT" in g_IndiDict[anIndi]:
            deathDT = datetime.strptime(g_IndiDict[anIndi]["DEAT"], "%d %b %Y")

            if deathDT >= today:
                valid = False

        #If we fail the test, append error to errors
        if not valid:
            #AppendDictStr("ERROR", g_IndiDict[anIndi], "US01", ",")
            errors.append("Error US01: One or more of the dates associated with " + \
                           "(" + anIndi + ") occurs after today.")

    for aFam in g_FamDict.keys():
        valid = True

        marrDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        if marrDT >= today:
            valid = False

        if "DIV" in g_FamDict[aFam]:
            divDT = datetime.strptime(g_FamDict[aFam]["DIV"], "%d %b %Y")

            if divDT >= today:
                valid = False

                #If we fail the test, append error to errors
        if not valid:
            #AppendDictStr("ERROR", g_FamDict[aFam], "US01", ",")
            errors.append("Error US01: One or more of the dates associated with " + \
                           "(" + aFam + ") occurs after today.")
        
    return errors


#User Story 02 Birth before marriage
def US02Validation():
    errors = []

    for aFam in g_FamDict.keys():
        valid = True
        
        marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        theWife = g_FamDict[aFam]["WIFE"]
        theHusb = g_FamDict[aFam]["HUSB"]

        if theWife in g_IndiDict:
            wifeBirthDT = datetime.strptime(g_IndiDict[theWife]["BIRT"], "%d %b %Y")

            if wifeBirthDT >= marriageDT:
                valid = False
            
        else:
            valid = False

        if theHusb in g_IndiDict:
            husbBirthDT = datetime.strptime(g_IndiDict[theHusb]["BIRT"], "%d %b %Y")

            if husbBirthDT >= marriageDT:
                valid = False
            
        else:
            valid = False

        # if not valid:
        #     AppendDictStr("ERROR", aFam, "US02", ",")
        #If we fail the test, append error to errors
        if not valid:
            errors.append("Error US02: One or more of the birthdates associated with the married couple" + \
                           " (" + theWife + ") and (" + theHusb + \
                            ") in (" + aFam + ") occurs after the date of their marriage.")
    return errors

#User Story 03 Birth before death
def US03Validation():
    errors = []

    for anIndi in g_IndiDict.keys():
        valid = True

        birthDT = None
        deathDT = None

        if "BIRT" in g_IndiDict[anIndi]:
            birthDT = datetime.strptime(g_IndiDict[anIndi]["BIRT"], "%d %b %Y")
        
        if "DEAT" in g_IndiDict[anIndi]:
            deathDT = datetime.strptime(g_IndiDict[anIndi]["DEAT"], "%d %b %Y")
        
        if birthDT and deathDT and deathDT <= birthDT:
            valid = False

        if not valid:
            errors.append("Error US03: Birth date of (" + anIndi + ")" + " occurs after their death date.")

    return errors

#User Story 04 Marriage before divorce
def US04Validation():
    errors = []
    
    for aFam in g_FamDict.keys():
        valid = True
            
        if "MARR" in g_FamDict[aFam] and "DIV" in g_FamDict[aFam]:
            marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")
            divorceDT = datetime.strptime(g_FamDict[aFam]["DIV"], "%d %b %Y")
            
            if divorceDT <= marriageDT:
                valid = False
        
        if not valid:
            #AppendDictStr("Error", g_FamDict[aFam], "US04", ",")
            errors.append("Error US04: The divorce date of family (" + aFam + ") occurs before their marriage date.")
    
    return errors

#User Story 05 Marriage before death
def US05Validation():
    errors = []

    for aFam in g_FamDict.keys():
        valid = True
    
        marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        try:
            theWife = g_FamDict[aFam]["WIFE"]
            theHusb = g_FamDict[aFam]["HUSB"]
        except:
            continue

        if theWife in g_IndiDict and "DEAT" in g_IndiDict[theWife]:
            wifeDeathDT = datetime.strptime(g_IndiDict[theWife]["DEAT"], "%d %b %Y")
            if wifeDeathDT < marriageDT:
                valid = False

        if theHusb in g_IndiDict and "DEAT" in g_IndiDict[theHusb]:
            husbDeathDT = datetime.strptime(g_IndiDict[theHusb]["DEAT"], "%d %b %Y")
            if husbDeathDT < marriageDT:
                valid = False
        
        if not valid:
            # AppendDictStr("ERROR", g_FamDict[aFam], "US05", ",")
            errors.append("Error US05: One or more of the death dates of" + \
                          " (" + theWife + ") and (" + theHusb + ") in family (" + aFam + ") occurs before the date of their marriage.")
    
    return errors

#User Story 06 Divorce before death
def US06Validation():
    errors = []

    for aFam in g_FamDict.keys():
        valid = True
    
        if "DIV" in g_FamDict[aFam]:
            divorceDT = datetime.strptime(g_FamDict[aFam]["DIV"], "%d %b %Y")

            try:
                theWife = g_FamDict[aFam]["WIFE"]
                theHusb = g_FamDict[aFam]["HUSB"]
            except:
                continue

            if theWife in g_IndiDict and "DEAT" in g_IndiDict[theWife]:

                wifeDeathDT = datetime.strptime(g_IndiDict[theWife]["DEAT"], "%d %b %Y")
                if wifeDeathDT < divorceDT:
                    valid = False

            if theHusb in g_IndiDict and "DEAT" in g_IndiDict[theHusb]:

                husbDeathDT = datetime.strptime(g_IndiDict[theHusb]["DEAT"], "%d %b %Y")
                if husbDeathDT < divorceDT:
                    valid = False

        if not valid:
            errors.append("Error US06: Divorce date of" + \
                          " (" + theWife + ") and ("  + theHusb + ")" \
                          + " in family (" + aFam + ") occurs before one of their death dates.")
    
    return errors

# User story 07 less than 150 years old
def US07Validation():
    errors = []

    for indi_id in g_IndiDict.keys():
        if 'BIRT' in g_IndiDict[indi_id]:
            birth_date = g_IndiDict[indi_id]['BIRT']
            age = calculate_age(birth_date, g_IndiDict[indi_id].get('DEAT'))
            if age >= 150:
                #AppendDictStr("ERROR", g_IndiDict[indi_id], f"ERROR: US07: {g_IndiDict[indi_id]['NAME']} ({indi_id}) is more than 150 years old", "\n")
                errors.append("Error US07: (" + indi_id + ") is more than 150 years old")
    
    return errors
                
# US08 Birth before Marriage of parents
def US08Validation():
    errors = []

    for fam_id in g_FamDict.keys():
        if "MARR" in g_FamDict[fam_id]:
            marriageDT = datetime.strptime(g_FamDict[fam_id]["MARR"], "%d %b %Y")

            for child_id in g_FamDict[fam_id].get("CHIL", []):
                if child_id in g_IndiDict and "BIRT" in g_IndiDict[child_id]:
                    birth_date = datetime.strptime(g_IndiDict[child_id]["BIRT"], "%d %b %Y")
                    # Emphasize birth before marriage
                    if birth_date <= marriageDT:
                        #AppendDictStr("ERROR", g_FamDict[fam_id], f"ERROR: US08: {g_IndiDict[child_id]['NAME']} ({child_id}) born before parents' marriage in family {fam_id}", "\n")
                        child_name = g_IndiDict[child_id].get('NAME', "Unknown")
                        errors.append(f"Error US08: {child_name} ({child_id}) born before or on the same day as parents' marriage in family ({fam_id}).")
        else:
            for child_id in g_FamDict[fam_id].get("CHIL", []):
                if child_id in g_IndiDict and "BIRT" in g_IndiDict[child_id]:
                    child_name = g_IndiDict[child_id].get("NAME","Unknown")
                    errors.append(f"Error US08: {child_name} ({child_id}) has no recorded marriage date for parents in family ({fam_id})")

    return errors

#09 Birth before death of parents
def US09Validation():
    errors = []
    for fam_id, family in g_FamDict.items():
        husband_id = family.get('HUSB')
        wife_id = family.get('WIFE')

        father_death_date = None
        mother_death_date = None

        if husband_id and husband_id in g_IndiDict:
            father_death = g_IndiDict[husband_id].get('DEAT')
            if father_death:
                father_death_date = parse_gedcom_date(father_death)

        if wife_id and wife_id in g_IndiDict:
            mother_death = g_IndiDict[wife_id].get('DEAT')
            if mother_death:
                mother_death_date = parse_gedcom_date(mother_death)

        for child_id in family.get('CHIL', []):
            if child_id in g_IndiDict:
                birth_date_str = g_IndiDict[child_id].get('BIRT')
                if birth_date_str:
                    birth_date = parse_gedcom_date(birth_date_str)
                    if mother_death_date and birth_date and birth_date > mother_death_date:
                        errors.append(f"Error US09: Child {child_id} born after mother's death.")
                    if father_death_date and birth_date and birth_date > father_death_date + timedelta(days=9*30):
                        errors.append(f"Error US09: Child {child_id} born more than 9 months after father's death.")
    return errors

# US10 No marriage before 14
def US10Validation():
    errors = []

    for aFam in g_FamDict.keys():
        if "MARR" in g_FamDict[aFam]:
            marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")
            marriageStr = marriageDT.strftime("%d %b %Y")
            
            if "WIFE" in g_FamDict[aFam] and "HUSB" in g_FamDict[aFam]:
                theWife = g_FamDict[aFam]["WIFE"]
                theHusb = g_FamDict[aFam]["HUSB"]

                if theWife in g_IndiDict and "BIRT" in g_IndiDict[theWife]:
                    wifeBirthDT = datetime.strptime(g_IndiDict[theWife]["BIRT"], "%d %b %Y")
                    wifeBirthStr = wifeBirthDT.strftime("%d %b %Y")
                    
                    if calculate_age(wifeBirthStr,marriageStr) < 14:
                        theWifeName = g_IndiDict[theWife].get("NAME", "Unknown")
                        theHusbName = g_IndiDict[theHusb].get("NAME", "Unknown")                    
                        errors.append(f"Anomaly US10: Age of {theWife} ({theWife}) is less than 14" + \
                                        f" at the time of her marriage to {theHusbName} ({theHusb}).")

                if theHusb in g_IndiDict and "BIRT" in g_IndiDict[theHusb]:
                    husbBirthDT = datetime.strptime(g_IndiDict[theHusb]["BIRT"], "%d %b %Y")
                    husbBirthStr = husbBirthDT.strftime("%d %b %Y")
                    
                    if calculate_age(husbBirthStr,marriageStr) < 14:
                        theWifeName = g_IndiDict[theWife].get("NAME", "Unknown")
                        theHusbName = g_IndiDict[theHusb].get("NAME", "Unknown")
                        errors.append(f"Anomaly US10: Age of {theHusb} ({theHusb}) is less than 14" + \
                                        f" at the time of his marriage to {theWifeName} ({theWife}).")
            
    return errors

# US12 Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
def US12Validation():
    errors = []
    
    for fam_id in g_FamDict.keys():
        family = g_FamDict[fam_id]
        if "HUSB" in family and "WIFE" in family and "CHIL" in family:
            husband_id = family["HUSB"]
            wife_id = family["WIFE"]

            for child_id in family["CHIL"]:
                child_birth_date = get_individual_birth_date(child_id)
                if child_birth_date:
                    if not validate_parent_child_age_difference(wife_id, child_birth_date, 60):
                        errors.append(f"Error US12: Mother ({wife_id}) in family ({fam_id}) is more than 60 years older than child ({child_id}).")
                    if not validate_parent_child_age_difference(husband_id, child_birth_date, 80):
                        errors.append(f"Error US12: Father ({husband_id}) in family ({fam_id}) is more than 80 years older than child ({child_id}).")
    
    return errors

# US13 Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
def US13Validation():
    errors = []
    
    for fam_id, family in g_FamDict.items():
        if "CHIL" in family:
            sibling_birth_dates = []
            for child_id in family['CHIL']:
                birthdate = get_individual_birth_date(child_id)
                if birthdate:
                    sibling_birth_dates.append((child_id, birthdate))
            
            sibling_birth_dates.sort(key=lambda x: x[1])
            
            for i in range(len(sibling_birth_dates) - 1):
                diff_days = (sibling_birth_dates[i + 1][1] - sibling_birth_dates[i][1]).days
                if not (diff_days < 2 or diff_days >= 8 * 30):
                    errors.append(f"Error US13: Sibling birth dates in family ({fam_id}) are not sufficiently spaced: {sibling_birth_dates[i][0]} and {sibling_birth_dates[i + 1][0]}.")
    return errors

# US14 No more than 5 siblings should be born at the same time
def US14Validation():

    # g_IndiDict["@I52@"] = {"BIRT": "01 JAN 2002"}
    # g_IndiDict["@I53@"] = {"BIRT": "01 JAN 2002"}
    # g_IndiDict["@I54@"] = {"BIRT": "01 JAN 2002"}
    # g_IndiDict["@I55@"] = {"BIRT": "01 JAN 2002"}
    # g_IndiDict["@I56@"] = {"BIRT": "01 JAN 2002"}
    # g_IndiDict["@I57@"] = {"BIRT": "02 MAR 2007"}
    # g_FamDict["@F55@"] = {"CHIL": ["@I52@", "@I53@", "@I54@", "@I55@", "@I56@", "@I57@"]}

    errors = []

    for aFam in g_FamDict.keys():

        valid_siblings = True
    
        if 'CHIL' in g_FamDict[aFam]:

            if len(g_FamDict[aFam]['CHIL']) >= 5:

                birthdays = []

                # for child in children
                try:
                    for indi_id in g_FamDict[aFam]['CHIL']:
                        if 'BIRT' in g_IndiDict[indi_id].keys():
                            birth = datetime.strptime(g_IndiDict[indi_id]["BIRT"], "%d %b %Y")
                            birthdays.append(birth)

                            if birthdays.count(birth) >= 5:
                                valid_siblings = False
                except:
                    #except to catch Key Error: '@'
                    pass

        if not valid_siblings:
            errors.append(f"Anomaly US14: 5 or more siblings in family {aFam} were born at the same time.")
    
    return errors

# US15 There should be fewer than 15 siblings in a family
def US15Validation():
    errors = []

    valid = True

    for fam_id in g_FamDict.keys():

        if "CHIL" in g_FamDict[fam_id]:
            childStr = g_FamDict[fam_id]["CHIL"]

            numAts = 0

            for aChar in childStr:
                if '@' == aChar:
                    numAts += 1

            numChildren = numAts / 2

            if numChildren > 14:
                valid = False

    if not valid:
        #AppendDictStr("ERROR", g_FamDict[fam_id], f"ERROR: US08: {g_IndiDict[child_id]['NAME']} ({child_id}) has no recorded marriage date for parents in family {fam_id}", "\n")
        errors.append("Error US15: family (" + fam_id + ") has 15 or more siblings!\n")
    
    return errors

# US21 Husband in family should be male and wife in family should be female
def US21Validation():
    errors = []

    valid = True

    for fam_id in g_FamDict.keys():
        if "HUSB" in g_FamDict[fam_id]:
            husbID = g_FamDict[fam_id]["HUSB"]

            if husbID in g_IndiDict and "SEX" in g_IndiDict[husbID]:
                if not g_IndiDict[husbID]["SEX"].upper == "M":
                    valid = False

        if "WIFE" in g_FamDict[fam_id]:
            wifeID = g_FamDict[fam_id]["WIFE"]

            if wifeID in g_IndiDict and "SEX" in g_IndiDict[wifeID]:
                if not g_IndiDict[wifeID]["SEX"].upper == "F":
                    valid = False
            
    if not valid:
        #AppendDictStr("ERROR", g_FamDict[fam_id], f"ERROR: US08: {g_IndiDict[child_id]['NAME']} ({child_id}) has no recorded marriage date for parents in family {fam_id}", "\n")
        errors.append("Error US21: family (" + fam_id + ") incorrect gender roles!\n")
    
    return errors

def US22Validation():
    errors = []
    valid = True

    #Dictionaries don't allow duplicate keys, so we'll verify that the fam and indi dicts don't have duplicate keys
    for aKey in g_IndiDict.keys():
        if aKey in g_FamDict.keys():
            valid = False

    if not valid:
        errors.append("Error US22: duplicate keys found between g_IndiDict and g_FamDict!\n")

    return errors

# US24 No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
def US24Validation():
    errors = []

    families = []

    for aFam in g_FamDict.keys():

        if "MARR" in g_FamDict[aFam].keys() and "HUSB" in g_FamDict[aFam].keys() and "WIFE" in g_FamDict[aFam].keys():
            
            theWife = g_FamDict[aFam]["WIFE"]
            theHusb = g_FamDict[aFam]["HUSB"]
            marriageDT = g_FamDict[aFam]["MARR"]

            fam = [marriageDT, theWife, theHusb]

            if fam in families:
                errors.append(f"Error US24: The family consisting of {theWife} and {theHusb} ({marriageDT}) is duplicated.")
            else:
                families.append(fam)

    return errors

# US26 All family roles (spouse, child) specified in an individual record should have corresponding entries in
# the corresponding family records. Likewise, all individual roles (spouse, child) specified in family
# records should have corresponding entries in the corresponding  individual's records. 
# I.e. the information in the individual and family records should be consistent.
def US26Validation():
    errors = []
    # Check invididuals for FAMC in Families in the list under CHIL
    for anIndi in g_IndiDict.keys():
        if 'FAMC' in g_IndiDict[anIndi].keys():
            family_of_chil = g_IndiDict[anIndi]['FAMC']
            if  family_of_chil not in g_FamDict \
                or 'CHIL' not in g_FamDict[family_of_chil].keys() \
                or anIndi not in g_FamDict[family_of_chil]['CHIL']:
                errors.append(f'Error US26: Individual {anIndi} is listed as a child of {family_of_chil} but is' + \
                              'not present in that family.')
    
    # Check individuals for FAMS in Families under HUSB or WIFE
    for anIndi in g_IndiDict.keys():
        if 'FAMS' in g_IndiDict[anIndi].keys():
            family_of_spou = g_IndiDict[anIndi]['FAMS']
            if  family_of_spou not in g_FamDict \
                or 'CHIL' not in g_FamDict[family_of_spou].keys() \
                or (anIndi != g_FamDict[family_of_spou]['HUSB'] and anIndi != g_FamDict[family_of_spou]['WIFE']):
                errors.append(f'Error US26: Individual {anIndi} is listed as a spouse in {family_of_spou} but is' + \
                              'not present in that family.')
    
    # Check families for HUSB in Individ with FAMS
    for aFam in g_FamDict.keys():
        if 'HUSB' in g_FamDict[aFam].keys():
            husb_of_fam = g_FamDict[aFam]['HUSB']
            if husb_of_fam not in g_IndiDict \
            or 'FAMS' not in g_IndiDict[husb_of_fam].keys() \
            or aFam != g_IndiDict[husb_of_fam]['FAMS']:
                errors.append(f'Error US26: Husband {husb_of_fam} of family {aFam} is not accounted for with proper' + \
                              'FAMS tag in individuals list.')

    # Check families for WIFE in Individ with FAMS
    for aFam in g_FamDict.keys():
        if 'WIFE' in g_FamDict[aFam].keys():
            wife_of_fam = g_FamDict[aFam]['WIFE']
            if wife_of_fam not in g_IndiDict \
            or 'FAMS' not in g_IndiDict[wife_of_fam].keys() \
            or aFam != g_IndiDict[wife_of_fam]['FAMS']:
                errors.append(f'Error US26: Wife {wife_of_fam} of family {aFam} is not accounted for with proper' + \
                              'FAMS tag in individuals list.')

    # Check families for CHIL in Invivid with FAMC
    for aFam in g_FamDict.keys():
        if 'CHIL' in g_FamDict[aFam].keys():
            children = g_FamDict[aFam]['CHIL']
            for child in children:
                if child not in g_IndiDict \
                or 'FAMC' not in g_IndiDict[child].keys() \
                or aFam != g_IndiDict[child]['FAMC']:
                    errors.append(f'Error US26: Child {child} of family {aFam} is not accounted for with proper' + \
                                'FAMC tag in individuals list.')

    return errors

#Takes in a list of stringLists and prints every string
def printQueue(stringListList):
    for list in stringListList:
        for string in list:
            print(string)

def DataValidation():
    errorQueue = []

    errorQueue.append(US01Validation())
    errorQueue.append(US02Validation())
    errorQueue.append(US03Validation())
    errorQueue.append(US04Validation())
    errorQueue.append(US05Validation())
    errorQueue.append(US06Validation())
    errorQueue.append(US07Validation())
    errorQueue.append(US08Validation())
    errorQueue.append(US09Validation())
    errorQueue.append(US12Validation())
    errorQueue.append(US13Validation())
    errorQueue.append(US14Validation())
    errorQueue.append(US15Validation())
    errorQueue.append(US21Validation())
    errorQueue.append(US22Validation())
    errorQueue.append(US24Validation())
    errorQueue.append(US26Validation())


    printQueue(errorQueue)
    
    #...

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# File & Field Parsing Functions
#-------------------------------------------------------------------------------
def parse_gedcom_date(date_str):
    try:
        if date_str.startswith(('AFT', 'BEF', 'ABT')):
            parts = date_str.split(' ', 1)
            date_str = parts[1]
        return datetime.strptime(date_str, '%d %b %Y')
    except ValueError:
        return None

def ParseData(inFile):
    indID  = ""
    famID  = ""

    with open(inFile, 'r') as fileData:
        inputLine = fileData.readline()

        while len(inputLine) > 0: 
      
            strLevel, strTag, strData = ParseFields(inputLine)

            #Removing @ symbols and slashes from string data
            strData = strData.replace('@', '')
            strData = strData.replace('/', '')

            #Individuals Top Level
            if "0" == strLevel and "INDI" == strTag:
                #Close last tag (*)
                famID = ""
                #Generate a new dictionary entry for the new individual
                indID = strData
                g_IndiDict[indID] = {}

            #Families Top Level
            elif "0" == strLevel and "FAM" == strTag:
                
                indID = ""
                
                famID = strData
                g_FamDict[famID] = {}

            elif "1" == strLevel and ("" != indID or "" != famID):
                
                if strTag in ["BIRT", "DEAT", "MARR", "DIV"]:
                    
                    inputLine = fileData.readline()
                    strLevel2, strTag2, strData2 = ParseFields(inputLine)

                    if "2" == strLevel2 and "DATE" == strTag2:
                        if "" != indID:
                            g_IndiDict[indID][strTag] = strData2
                        elif "" != famID:
                            g_FamDict[famID][strTag] = strData2
                    else:
                        #Format error!
                        pass
                    
                elif "CHIL" == strTag:
                    if "CHIL" in g_FamDict[famID]:
                        g_FamDict[famID]["CHIL"].append(strData)
                    else:
                        g_FamDict[famID]["CHIL"] = [strData]
                        
                elif strTag in lstValidTags:
                    if "" != indID:
                        g_IndiDict[indID][strTag] = strData
                    elif "" != famID:
                        g_FamDict[famID][strTag] = strData
                else:
                    #Format error!
                    pass

            inputLine = fileData.readline()

def ParseFields(inLine):
    dataList = inLine.split(" ")

    #First we will parse our tag out into these string variables for later evaluation
    strLevel = dataList[0]
    strTag   = ""
    strData  = ""
    
    if len(dataList) > 1:  
        #Check if this is a 2 or 3+ field line
        if 2 == len(dataList):
            strTag = dataList[1].strip()
        else:
            #Check for INDI/FAM out of order + length of data list
            if len(dataList) > 2 and dataList[2].strip() in ["INDI", "FAM"]:       
                #This is a special case where the tag is 3rd and data is 2nd
                strData = dataList[1].strip()
                strTag  = dataList[2].strip()
            else:
                #This is a standard tag
                strTag  = dataList[1].strip()
                strData = " ".join(dataList[2:]).strip()

    return [strLevel, strTag, strData]

def ParseData(inFile):
    indID  = ""
    famID  = ""

    with open(inFile, 'r') as fileData:
        inputLine = fileData.readline()

        while len(inputLine) > 0: 
      
            strLevel, strTag, strData = ParseFields(inputLine)

            #Removing @ symbols and slashes from string data
            strData = strData.replace('@', '')
            strData = strData.replace('/', '')

            #Individuals Top Level
            if "0" == strLevel and "INDI" == strTag:
                #Close last tag (*)
                famID = ""
                #Generate a new dictionary entry for the new individual
                indID = strData
                g_IndiDict[indID] = {}

            #Families Top Level
            elif "0" == strLevel and "FAM" == strTag:
                #Close last tag (*)
                indID = ""
                #Generate a new dictionary entry for the new family
                famID = strData
                g_FamDict[famID] = {}

            elif "1" == strLevel and ("" != indID or "" != famID):
                #Check if this is a single line dataset or two
                if strTag in ["BIRT", "DEAT", "MARR", "DIV"]:
                    #This tag uses a second data line we'll process another line of data
                    inputLine = fileData.readline()
                    strLevel2, strTag2, strData2 = ParseFields(inputLine)

                    if "2" == strLevel2 and "DATE" == strTag2:
                        if "" != indID:
                            g_IndiDict[indID][strTag] = strData2
                        elif "" != famID:
                            g_FamDict[famID][strTag] = strData2
                    else:
                        #Format error!
                        pass
                    
                #Check if it's children as we'll need to append to the existing family children data
                elif "CHIL" == strTag:
                    if "CHIL" in g_FamDict[famID]:
                        g_FamDict[famID]["CHIL"] += ", " + strData
                    else:
                        g_FamDict[famID]["CHIL"] = strData
                        
                elif strTag in lstValidTags:
                    if "" != indID:
                        g_IndiDict[indID][strTag] = strData
                    elif "" != famID:
                        g_FamDict[famID][strTag] = strData
                else:
                    #Format error!
                    pass

            inputLine = fileData.readline()
            
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Table Functions
#-------------------------------------------------------------------------------
def BuildTables():
    g_IndividualsTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    g_FamiliesTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]   
    
    #Build the individuals entries
    for anIndiID in g_IndiDict.keys():
        listData = []
        listData.append(anIndiID)                                           #ID
        listData.append(g_IndiDict[anIndiID]["NAME"])                       #Name
        listData.append(g_IndiDict[anIndiID]["SEX"])                        #Gender
        listData.append(g_IndiDict[anIndiID]["BIRT"])                       #Birthday
    
        isAlive = not "DEAT" in g_IndiDict[anIndiID]

        #Perform age calculation using datetime module
        ageValue = 0
        birthDT = datetime.strptime(g_IndiDict[anIndiID]["BIRT"], "%d %b %Y")
        
        if isAlive:
            ageValue = AgeDateTimeCalc(birthDT, datetime.today())
        else:
            deathDT = datetime.strptime(g_IndiDict[anIndiID]["DEAT"], "%d %b %Y")
            ageValue = AgeDateTimeCalc(birthDT, deathDT)
            

        listData.append(str(ageValue))                                      #Age
            
        listData.append(str(isAlive))                                       #Alive
        listData.append("NA" if isAlive else g_IndiDict[anIndiID]["DEAT"])  #Death

        isChild = "FAMC" in g_IndiDict[anIndiID]
        listData.append(g_IndiDict[anIndiID]["FAMC"] if isChild else "NA")  #Child

        isSpouse = "FAMS" in g_IndiDict[anIndiID]
        listData.append(g_IndiDict[anIndiID]["FAMS"] if isSpouse else "NA") #Spouse

        g_IndividualsTable.add_row(listData)

    #Build the families entries
    for aFamID in g_FamDict.keys():
        listData = []

        listData.append(aFamID)                                                                  #ID
        listData.append(g_FamDict[aFamID]["MARR"] if "MARR" in g_FamDict[aFamID] else "Missing") #Married
        listData.append(g_FamDict[aFamID]["DIV"] if "DIV" in g_FamDict[aFamID] else "NA")        #Divorced

        husbID = g_FamDict[aFamID]["HUSB"]
        listData.append(husbID)                                                                  #Husband
        listData.append(g_IndiDict[husbID]["NAME"])                                              #Husband Name

        wifeID = g_FamDict[aFamID]["WIFE"]
        listData.append(wifeID)                                                                  #Wife
        listData.append(g_IndiDict[wifeID]["NAME"])                                              #Wife Name

        listData.append(g_FamDict[aFamID]["CHIL"] if "CHIL" in g_FamDict[aFamID] else "NA")      #Children

        g_FamiliesTable.add_row(listData)
        
def PrintTables():    
    print("Individuals")
    print(g_IndividualsTable)

    print("Families")
    print(g_FamiliesTable)

    print("\n\n")

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# List User Story Functions
#-------------------------------------------------------------------------------
def List_US27():
    ageList = []
    
    for anIndiID in g_IndiDict.keys():
        indi = g_IndiDict[anIndiID]
        name = indi.get("NAME", "Unknown")
        birth_date = indi.get("BIRT", "Unknown")
        death_date = indi.get("DEAT", None)
    
        if birth_date != "Unknown":
            age = calculate_age(birth_date, death_date)
            ageList.append(f"{name} ({anIndiID}): Age {age}")

    print("List of all individuals and their age:")
    for indi in ageList:
        print(indi)
    print("\n")

def List_US28():
    siblings_by_age = {}

    for fam_id, family in g_FamDict.items():
        if "CHIL" in family:
            children = family["CHIL"]
            sibling_ages = []
            
            for child_id in children:
                child_details = g_IndiDict.get(child_id, {})
                name = child_details.get("NAME", "Unknown")
                birth_date = child_details.get("BIRT", None)
                death_date = child_details.get("DEAT", None)

                if birth_date:
                    age = calculate_age(birth_date, death_date)
                    sibling_ages.append((name, age))

            sibling_ages.sort(key=lambda x: x[1], reverse=True)
            siblings_by_age[fam_id] = sibling_ages

    print("List of siblings in families by decreasing age:")
    for fam_id, siblings in siblings_by_age.items():
        if siblings:
            print(f"Family {fam_id}:")
            for sibling in siblings:
                    print(f"  {sibling[0]}: Age {sibling[1]}")
    print("\n")
            
def List_US29():
    deadList = []
    
    for anIndiID in g_IndiDict.keys():
        if "DEAT" in g_IndiDict[anIndiID]:
            deadList.append(g_IndiDict[anIndiID]["NAME"])

    deadList = list(set(deadList))

    print("List of all deceased individuals:")
    print(deadList)
    print("\n")
    
            
def List_US30():
    liveMarried = []

    for aFamID in g_FamDict.keys():
        husbID = g_FamDict[aFamID]["HUSB"]
        wifeID = g_FamDict[aFamID]["WIFE"]

        indiKeys = g_IndiDict.keys()

        if husbID in indiKeys:
            if "DEAT" not in g_IndiDict[husbID]:
                liveMarried.append(g_IndiDict[husbID]["NAME"])

        if wifeID in indiKeys:
            if "DEAT" not in g_IndiDict[wifeID]:
                liveMarried.append(g_IndiDict[wifeID]["NAME"])

    liveMarried = list(set(liveMarried))

    print("List of all living and married individuals:")
    print(liveMarried)
    print("\n")

def List_US31():
    liveSingle = []

    for indi_id, indi in g_IndiDict.items():
        if 'DEAT' not in indi and 'FAMS' not in indi:
            liveSingle.append(indi["NAME"])

    liveSingle = list(set(liveSingle))

    print("List of all living and single individuals:")
    print(liveSingle)
    print("\n")

    return liveSingle

def List_US32():
    multiple_births = defaultdict(list)

    for fam_id, family in g_FamDict.items():
        if "CHIL" in family:
            children = family["CHIL"]
            birth_dates = defaultdict(list)
    
            for child_id in children:
                child_details = g_IndiDict.get(child_id, {})
                birth_date = child_details.get("BIRT", None)
                if birth_date:
                    birth_dates[birth_date].append(child_id)

            for birth_date, siblings in birth_dates.items():
                if len(siblings) > 1:
                    multiple_births[fam_id].append((birth_date, siblings))

    print("List of all multiple births:")
    for fam_id, birth_info in multiple_births.items():
        for birth_date, siblings in birth_info:
            print(f"Family {fam_id} has multiple births on {birth_date}: {', '.join(siblings)}")
    print("\n")
    return multiple_births

# US38 List Upcoming Birthdays
def List_US38():
    upcoming = []

    today = datetime.today()

    for indi_id in g_IndiDict.keys():
        if 'DEAT' not in g_IndiDict[indi_id].keys():
            indi_birth = get_individual_birth_date(indi_id)
            indi_birth = indi_birth.replace(year=today.year)

            differenceDT = indi_birth - today
            within30 = (differenceDT.days % 365) <= 30

            if within30:
                birthday_announcement = f"Individual {indi_id}: {g_IndiDict[indi_id]['NAME']}"
                upcoming.append(birthday_announcement)

    print("List of all upcoming birthdays:")
    for u in upcoming:
        print(u)
    print("\n")
    
    return upcoming

# US39 List Upcoming Anniversaries
def List_US39():
    upcoming = []

    today = datetime.today()

    for fam_id in g_FamDict.keys():
        if 'DIV' not in g_FamDict[fam_id].keys():

            #check both partners alive
            husb_id = g_FamDict[fam_id]['HUSB']
            wife_id = g_FamDict[fam_id]['WIFE']

            if 'DEAT' not in g_IndiDict[husb_id].keys() and 'DEAT' not in g_IndiDict[wife_id].keys():
                anniversary = datetime.strptime(g_FamDict[fam_id]["MARR"], "%d %b %Y")

                anniversary = anniversary.replace(year=today.year)

                differenceDT = anniversary - today
                within30 = (differenceDT.days % 365) <= 30

                if within30:
                    anni_announcement = f"Family {fam_id}: {g_IndiDict[husb_id]['NAME']} and {g_IndiDict[wife_id]['NAME']}"
                    upcoming.append(anni_announcement)

    print("List of all upcoming wedding anniversaries:")
    for u in upcoming:
        print(u)
    print("\n")
    
    return upcoming
#US37 : List all recent survivors
def List_US37():
    recent_deaths = []
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    for indi_id, indi in g_IndiDict.items():
        if "DEAT" in indi:
            death_date = datetime.strptime(indi["DEAT"], "%d %b %Y")
            if thirty_days_ago <= death_date <= today:
                family_id = indi.get("FAMS", None)
                survivors = []
                if family_id:
                    family = g_FamDict.get(family_id, {})
                    if "HUSB" in family and family["HUSB"] != indi_id:
                        survivors.append(g_IndiDict[family["HUSB"]]["NAME"])
                    if "WIFE" in family and family["WIFE"] != indi_id:
                        survivors.append(g_IndiDict[family["WIFE"]]["NAME"])
                    if "CHIL" in family:
                        for child_id in family["CHIL"]:
                            survivors.append(g_IndiDict[child_id]["NAME"])
                recent_deaths.append({"name": indi["NAME"], "survivors": survivors})

    survivors_list = []
    for entry in recent_deaths:
        survivors_list.extend(entry['survivors'])

    print("List of recent survivors:")
    for survivor in survivors_list:
        print(survivor)
    print("\n")
    return survivors_list

#US42:reject all illegitimate dates
def List_US42():
    errors = [] 

    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%d %b %Y')
            return True
        except ValueError:
            return False

    for indi_id, indi in g_IndiDict.items():
        if "BIRT" in indi and not is_valid_date(indi["BIRT"]):
            errors.append(f"Error US42: Individual {indi_id} has an invalid birth date.")
        if "DEAT" in indi and not is_valid_date(indi["DEAT"]):
            errors.append(f"Error US42: Individual {indi_id} has an invalid death date.")
    
    for fam_id, fam in g_FamDict.items():
        if "MARR" in fam and not is_valid_date(fam["MARR"]):
            errors.append(f"Error US42: Family {fam_id} has an invalid marriage date.")
        if "DIV" in fam and not is_valid_date(fam["DIV"]):
            errors.append(f"Error US42: Family {fam_id} has an invalid divorce date.")

    print("List of all invalid dates:")
    for error in errors:
        print(error)
    return errors

#Recent births (30 days)
def List_US35():
    birthList = []
    
    for anIndiID in g_IndiDict.keys():
        indi = g_IndiDict[anIndiID]
        name = indi.get("NAME", "Unknown")
        birth_date = indi.get("BIRT", "Unknown")
    
        if birth_date != "Unknown":
            ageDays = calculate_days(birth_date)

            if(30 >= ageDays):
                birthList.append(namne)

    print("List of all individuals born recently:")
    for indi in birthList:
        print(indi)
    print("\n")

    return birthList

#Recent deaths (30 days)
def List_US36():
    deathList = []
    
    for anIndiID in g_IndiDict.keys():
        indi = g_IndiDict[anIndiID]
        name = indi.get("NAME", "Unknown")
        death_date = indi.get("DEAT", "Unknown")
    
        if death_date != "Unknown":
            deathDays = calculate_days(death_date)

            if(30 >= deathDays):
                deathList.append(namne)

    print("List of all recently deceased:")
    for indi in deathList:
        print(indi)
    print("\n")

    return deathList


def PrintLists():
    List_US27()
    List_US28()
    List_US29()
    List_US30()
    List_US31()
    List_US32()
    List_US37()
    List_US38()
    List_US39()
    List_US42()
    List_US35()
    List_US36()
    #...

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    ParseData('Group1.ged')
    BuildTables()
    PrintTables()
    PrintLists()
    

