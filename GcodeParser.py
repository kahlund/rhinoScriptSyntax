import rhinoscriptsyntax as rs

newLines = []
extrude1 = "A"
extrude2 = " B"
extMove =  "E"
moveCode = "G1"
extCode = "G92 E0"
zMove = "Z"
zLiftHeight = "5"
feedCode = "F"
fileType = ".gcode"

def ImportGCode():
    #prompt the user for a file to import
    filter = "Text file (*.gcode)|*.gcode|All Files (*.*)|*.*||"
    filename = rs.OpenFileName("Open Point File", filter)
    if not filename: return

    #read each line from the file
    file = open(filename, "r")
    gCode = file.readlines()
    file.close()
    length = len(gCode)
    i = 0
    #iterate through each item in the array
    for line in gCode: 
        i = i + 1
        print str(i) + " out of " + str(length)
        feedBol = False
        dist = 0
        feedRate = []
        line = line.strip("\n")
        tempLine = []
        tLine = []
        if  extCode in line:
            newLines.append("G92 A0 B0 \n" )
            continue
        if not moveCode in line:                 #If there is no G1 command in the line, add line to temp line array and go to next line
            newLines.append(line + "\n") 
            continue 
        if zMove in line:
            tempZMove = line.split("F")[0]
            tempFeed = line.split("F")[-1]
            tempZMove = tempZMove.split("Z")[-1]
            tempZMoveDist = float(tempZMove) + float(zLiftHeight)
            newLines.append("G1 Z" + str(tempZMoveDist) + " F" + tempFeed + "\n")
            newLines.append(line.split("Z")[0] + " Z" + str(tempZMoveDist) + "\n")
            newLines.append("G1 Z" + str(tempZMove) + " F" + tempFeed + "\n")
            continue
        if not extMove in line:                  
            newLines.append(line + "\n")
            continue
        if feedCode in line:
            feedBol = True
        extValue = line.split('E')[-1]          #G1 X??? Y??? Z??? E??? F??? because we know this is the format of g1, we split the line at "E" and take second half, leaving the distance of travel and Feedrate
        tempLine = line.split('E')[0] 
        extValue = extValue.split('F')[0]           #G1 X??? Y??? Z??? E??? F??? because we know this is the format of g1, we split the line at "F" and take first half which is only the distance of travel
        feedRate = "F" + str(line.split('F')[-1])
        extValue = extValue.strip("\n")         #Removes new line "\n"
        tempLine = tempLine.strip("\n")         #Removes new line "\n"
        if feedBol == True:
            replacement =  tempLine + extrude1 + str(extValue) + extrude2 + str(extValue) + feedRate
        else:
            replacement =  tempLine + extrude1 + str(extValue) + extrude2 + str(extValue)
        replacement = replacement + "\n"
        newLines.append(replacement)
    return newLines, filename.strip(".gcode")

def writeNewGCode(newLines, filename):
    with open(filename + "DoubleExtruder" + fileType, "w") as output:
        output.writelines(newLines)

if( __name__ == "__main__" ):
    gCode, filename = ImportGCode()
    writeNewGCode(gCode, filename)
