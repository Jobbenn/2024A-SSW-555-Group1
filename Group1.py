#Group 1 collab session 6/8/2024

from prettytable import PrettyTable

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


def ParseFields(inLine):
    dataList = inLine.split(" ")

    #First we will parse our tag out into these string variables for later evaluation
    strLevel = dataList[0]
    strTag   = ""
    strData  = ""
        
    #Check if this is a 2 or 3+ field line
    if 2 == len(dataList):
        strTag = dataList[1].strip()
    else:
        #Check for INDI/FAM out of order
        if dataList[2].strip() in ["INDI", "FAM"]:
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
                    
                elif strTag in lstValidTags:
                    if "" != indID:
                        g_IndiDict[indID][strTag] = strData
                    elif "" != famID:
                        g_FamDict[famID][strTag] = strData
                else:
                    #Format error!
                    pass

            inputLine = fileData.readline()


def PrintTables():
    #g_IndividualsTable.field_names = ["ID", "Name", "Gender", "Birthday", "Death", "Child", "Husband", "Wife", "Divorce"]
    #g_FamiliesTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    
    #print("Individuals")
    #print(g_IndividualsTable)

    #print("Families")
    #print(g_FamiliesTable)

    print(g_IndiDict)
    print(g_FamDict)

if __name__ == '__main__':
    ParseData('Group1.ged')
    PrintTables()
