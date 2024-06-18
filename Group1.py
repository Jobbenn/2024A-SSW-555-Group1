#Group 1 Program

from prettytable import PrettyTable
from datetime import datetime

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
                    if birth_date < marriageDT:
                        #AppendDictStr("ERROR", g_FamDict[fam_id], f"ERROR: US08: {g_IndiDict[child_id]['NAME']} ({child_id}) born before parents' marriage in family {fam_id}", "\n")
                        errors.append(f"Error US08: {g_IndiDict[child_id]['NAME']} ({child_id}) born before parents' marriage in family ({fam_id}).")
        else:
            for child_id in g_FamDict[fam_id].get("CHIL", []):
                if child_id in g_IndiDict and "BIRT" in g_IndiDict[child_id]:
                    #AppendDictStr("ERROR", g_FamDict[fam_id], f"ERROR: US08: {g_IndiDict[child_id]['NAME']} ({child_id}) has no recorded marriage date for parents in family {fam_id}", "\n")
                    errors.append(f"Error US08: {g_IndiDict[child_id]['NAME']} ({child_id}) has no recorded marriage date for parents in family ({fam_id})")

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

    printQueue(errorQueue)
    
    #...

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# File & Field Parsing Functions
#-------------------------------------------------------------------------------

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
    DataValidation()
    BuildTables()
    PrintTables()
    
__all__ = [
    'US01Validation', 'US02Validation', 'US03Validation', 'US04Validation',
    'US05Validation', 'US06Validation', 'US07Validation', 'US08Validation',
    'g_IndiDict', 'g_FamDict', 'AppendDictStr'
]
