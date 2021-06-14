
# Created 14/06/2021
# @Author: Juraj Janekovic

def openFile(csv):
    with open(csv,'r') as myfile:
        lines = myfile.readlines()
    return lines

def sort(lines,OutFileSlve, OutFileMstr):
    mstrD = ""
    temp = []
    for line in lines:
        if len(line) > 2:
            if line[0] == "D":
                temp.append(line)
            else:
                mstrD += line
    temp.sort()
    index = 0
    x = False
    for i in range (1,len(temp)):
        if temp[i][2] != temp[index][2]:
            with open(temp[i-1][:2]+OutFileSlve[3:],'w') as myFile2:
                myFile2.write(temp[index:i])
            index = i
            x = True
    if not x:
        with open(temp[0][:3]+OutFileSlve[3:],'w') as myFile2:
            for line in temp: myFile2.write(line)
        
        
    with open(OutFileMstr,'w') as myFile1:
        myFile1.write(mstrD)

def main(filename):
    lines = openFile(filename)
    if filename[0] == 'm':
        OutFileSlve =  "D01_master_data.txt"
        OutFileMstr =  "master_data.txt"
    else:
        OutFileSlve =  "D01_servant_LoRa_data.txt"
        OutFileMstr =  "D01_servant_1s_data.txt"
    
    sort(lines,OutFileSlve, OutFileMstr)
    
    
    
            
