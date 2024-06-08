#Group 1 collab session 6/8/2024

from prettytable import PrettyTable

g_IndividualsTable = PrettyTable()
g_FamiliesTable = PrettyTable()

g_IndiDict = {}

lstSpecialTags = ["INDI",
                 "FAM"]

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

def BuildTableHeaders():
    g_IndividualsTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    g_FamiliesTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

    
def ParseIndividuals(inLine):
    tagList = inLine.split(" ")
    
    if tagList[0].isdigit():
        nLevel = int(tagList[0])

        strLevel = int(nLevel)
        strTag   = tagList[1].strip()
        strRest  = " ".join(tagList[2:])

        if (0 == nLevel) and (3 == len(tagList)) and (tagList[2].strip() in lstSpecialTags):
            #Special case for INDI or FAM
            strTag  = tagList[2].strip()
            strRest = tagList[1].strip()

        isValid = strTag in lstValidTags
        strReturn = "%s|%s|%s|%s" % (strLevel, strTag, strValid, strRest)

        dictUser = {"ID" : "", "Name" : "", "Gender" : "", "Birthday" : "", "Age" : "", "Alive" : "", "Death" : "", "Child" : "", "Spouse" : ""}

        g_IndiDict[UserID] = dictUser

def ParseFamilies(inLine):
    pass

def ParseDataFormat(inFile):

  with open(inFile, 'r') as fileData:
        for aLine in fileData.readlines():
            ParseFamilies(aLine)
            ParseIndividual(aLine)


def PrintTables():
    print("Individuals")
    print(g_InvidualsTable)

    print("Families")
    print(g_FamiliesTable)

if __name__ == '__main__':
    ParseDataFormat('Group1.ged')
    PrintTables()
