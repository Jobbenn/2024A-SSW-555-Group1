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
    if keyItem in dictItem:
        oldValueStr = dictItem[keyItem]
        dictItem[keyItem] = oldValueStr + spacerStr+ appendStr
    else:
        dictItem[keyItem] = appendStr
        
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Data Validation Functions
#-------------------------------------------------------------------------------

#User Story 01 Dates before current date
def US01Validation():
    today = datetime.today()

    for anIndi in g_IndiDict.keys():
        valid = True

        birthDT = datetime.strptime(g_IndiDict[anIndi]["BIRT"], "%d %b %Y")
        birthDelta = today - birthDT

        if 0 == birthDelta.days:
            valid = False
        
        if "DEAT" in g_IndiDict[anIndi]:
            deathDT = datetime.strptime(g_IndiDict[anIndi]["DEAT"], "%d %b %Y")
            deathDelta = today - deathDT

            if 0 == deathDelta.days:
                valid = False

        #If we fail the test append the error code
        if not valid:
            AppendDictStr("ERROR", g_IndiDict[anIndi], "US01", ",")

#User Story 02 Birth before marriage
def US02Validation():
    for aFam in g_FamDict.keys():
        valid = True
        
        marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        theWife = g_FamDict[aFam]["WIFE"]
        theHusb = g_FamDict[aFam]["HUSB"]

        if theWife in g_IndiDict:
            wifeBirthDT = datetime.strptime(g_IndiDict[theWife]["BIRT"], "%d %b %Y")
            deltaDT = marriageDT - wifeBirthDT

            if 0 == deltaDT.days:
                valid = False
            
        else:
            valid = False

        if theHusb in g_IndiDict:
            husbBirthDT = datetime.strptime(g_IndiDict[theHusb]["BIRT"], "%d %b %Y")
            deltaDT = marriageDT - husbBirthDT

            if 0 == deltaDT.days:
                valid = False
            
        else:
            valid = False

        if not valid:
            AppendDictStr("ERROR", aFam, "US02", ",")
            
#User Story 04 Marriage before divorce
def US04Validation():
    for aFam in g_FamDict.keys():
        valid = True
            
        if "MARR" in g_FamDict[aFam] and "DIV" in g_FamDict[aFam]:
            marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")
            divorceDT = datetime.strptime(g_FamDict[aFam]["DIV"], "%d %b %Y") 
            if divorceDT < marriageDT:
                valid = False
        
        if not valid:
            AppendDictStr("Error", g_FamDict[aFam], "US04", ",")

#User Story 05 Marriage before death
def US05Validation():
    for aFam in g_FamDict.keys():
        valid = True
    
    if "MARR" in g_FamDict[aFam]:
        marriageDT = datetime.strptime(g_FamDict[aFam]["MARR"], "%d %b %Y")

        theWife = g_FamDict[aFam]["WIFE"]
        theHusb = g_FamDict[aFam]["HUSB"]

        if theWife in g_IndiDict and "DEAT" in g_IndiDict[theWife]:
            wifeDeathDT = datetime.strptime(g_IndiDict[theWife]["DEAT"], "%d %b %Y")
            if wifeDeathDT < marriageDT:
                valid = False

        if theHusb in g_IndiDict and "DEAT" in g_IndiDict[theHusb]:
            husbDeathDT = datetime.strptime(g_IndiDict[theHusb]["DEAT"], "%d %b %Y")
            if husbDeathDT < marriageDT:
                valid = False

    if not valid:
        AppendDictStr("ERROR", g_FamDict[aFam], "US05", ",")

def DataValidation():
    US01Validation()
    US02Validation()
    US04Validation()
    US05Validation()
    
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
    g_IndividualsTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse", "Errors"]

    g_FamiliesTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children", "Errors"]   
    
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

        if "ERROR" in g_IndiDict[anIndiID]:
            listData.append(g_IndiDict[anIndiID]["ERROR"])
        else:
            listData.append("")

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

        if "ERROR" in g_FamDict[aFamID]:
            listData.append(g_FamDict[aFamID]["ERROR"])
        else:
            listData.append("")

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

