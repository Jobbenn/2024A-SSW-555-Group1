#Group 1 Program

from prettytable import PrettyTable
from datetime import datetime, timedelta

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
    for aFam in g_FamDict.keys():
        if "MARR" in g_FamDict[aFam]:
            marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        theWife = g_FamDict[aFam]["WIFE"]
        theHusb = g_FamDict[aFam]["HUSB"]

        if theHusb:
            father_death = g_IndiDict[theHusb].get('DEAT')
            if father_death:
             father_death_date = parse_gedcom_date(father_death) # type: ignore
            else:
                father_death_date = None

        if theWife:
            mother_death = g_IndiDict[theWife].get('DEAT')
            if mother_death:
                mother_death_date = parse_gedcom_date(mother_death) # type: ignore
            else:
                mother_death_date = None

        if "CHIL" in g_FamDict[aFam]:
            for child_id in g_FamDict[aFam]["CHIL"]:
                if child_id in g_IndiDict:
                    birth_date_str = g_IndiDict[child_id].get("BIRT")
                    if birth_date_str:
                        birth_date = parse_gedcom_date(birth_date_str) # type: ignore
                        if mother_death_date and birth_date > mother_death_date:
                            errors.append(f"Error US09: Child {child_id} born after mother's death.")
                        if father_death_date and birth_date > father_death_date + timedelta(days=9*30):
                            errors.append(f"Error US09: Child {child_id} born more than 9 months after father's death.")
                else:
                    print(f"Debug: Child ID {child_id} not found in individual dictionary.")
                    errors.append(f"Error US09: Child ID {child_id} not found in individual dictionary.")
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
        if "HUSB" in g_FamDict[fam_id] and "WIFE" in g_FamDict[fam_id] and "CHIL" in g_FamDict[fam_id]:
            husband_id = g_FamDict[fam_id]["HUSB"]
            wife_id = g_FamDict[fam_id]["WIFE"]

            if husband_id in g_IndiDict and wife_id in g_IndiDict:
                husband_birth_date = datetime.strptime(g_IndiDict[husband_id]["BIRT"], "%d %b %Y")
                wife_birth_date = datetime.strptime(g_IndiDict[wife_id]["BIRT"], "%d %b %Y")

                for child_id in g_FamDict[fam_id]["CHIL"]:
                    if child_id in g_IndiDict and "BIRT" in g_IndiDict[child_id]:
                        child_birth_date = datetime.strptime(g_IndiDict[child_id]["BIRT"], "%d %b %Y")
                        mother_age_at_birth = (child_birth_date - wife_birth_date).days / 365.25
                        father_age_at_birth = (child_birth_date - husband_birth_date).days / 365.25

                        if mother_age_at_birth >= 60:
                            errors.append(f"Error US12: Mother ({wife_id}) in family ({fam_id}) is more than 60 years older than child ({child_id}).")

                        if father_age_at_birth >= 80:
                            errors.append(f"Error US12: Father ({husband_id}) in family ({fam_id}) is more than 80 years older than child ({child_id}).")
    
    return errors

# US13 Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
def US13Validation():
    errors = []
    
    for fam_id, family in g_FamDict.items():
        if "CHIL" in family:
            sibling_birth_dates = []
            for child_id in family['CHIL']:
                if child_id in g_IndiDict and g_IndiDict[child_id] and g_IndiDict[child_id]["BIRT"] != "@":
                    birthdate = datetime.strptime(g_IndiDict[child_id]["BIRT"], "%d %b %Y")
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

    printQueue(errorQueue)
    
    #...

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# File & Field Parsing Functions
#-------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    ParseData('Group1.ged')
    BuildTables()
    PrintTables()
    

