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


def DecorateLine(inLine):
    tagList = inLine.split(" ")
    
    strReturn = "INVALID FORMAT"

    if tagList[0].isdigit():
        nLevel = int(tagList[0])

        strLevel = int(nLevel)
        strTag   = tagList[1].strip()
        strRest  = " ".join(tagList[2:])

        if (0 == nLevel) and (3 == len(tagList)) and (tagList[2].strip() in lstSpecialTags):
            #Special case for INDI or FAM
            strTag  = tagList[2].strip()
            strRest = tagList[1].strip()
            
        strValid  = "Y" if strTag in lstValidTags else "N"
        strReturn = "%s|%s|%s|%s" % (strLevel, strTag, strValid, strRest)
    
    return(strReturn)

def ParsePrintFormat(inFile):

  with open(inFile, 'r') as fileData:
        for aLine in fileData.readlines():
            print("--> %s" % (aLine), end='')
            print("<-- %s" % (DecorateLine(aLine)))

if __name__ == '__main__':
    ParsePrintFormat('Group1.ged')
