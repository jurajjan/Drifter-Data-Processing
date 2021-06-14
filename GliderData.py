
# Created 14/06/2021
# @Author: Juraj Janekovic

def openFile(csv):
    with open(csv,'r') as myfile:
        lines = myfile.readlines()
    return lines

def sort(lines):
    temp1 = ""
    temp2 = ""
    for line in lines:
        if len(line) != 0:
            line.strip('\n')
            if line[0] == "D":
                temp1 += line
            else: temp2 += line
    return temp1,temp2

def main(filename):
    lines = openFile(filename)
    temp1,temp2 = sort(lines)
    if filename[0] == 'm':
        OutFileD =  "D01_master_data.txt"
        OutFile2 =  "master_data.txt"
    else:
        OutFileD =  "D01_servant_LoRa_data.txt"
        OutFile2 =  "D01_servant_1s_data.txt"
    
    with open(OutFileD,'w') as myFile1:
        myFile1.write(temp1)
    
    with open(OutFile2,'w') as myFile2:
        myFile2.write(temp2)
    
    
    
            