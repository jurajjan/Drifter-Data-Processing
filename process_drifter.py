#!/usr/bin/env python

''' Created 14/06/2021
    Author: Juraj Janekovic
'''

def openFile(csv):
    with open(csv,'r', encoding = "ISO-8859-1") as myfile:
        lines = myfile.readlines()
    return lines

def sort(lines,OutFileSlve, OutFileMstr):
    mstrD = ""
    temp = []
    for line in lines:
        if len(line) > 2:
            try:
                if line[0] == "D" and line[27] != '0':
                    temp.append(line)
            except IndexError: continue
           
            else:
                try:
                    if line.split(',')[2] != '0.00000000' and line[0] == '2':
                        mstrD += line
                except IndexError: continue
    temp.sort()
    index = 0
    x = False
    for i in range (1,len(temp)):
        if temp[i][2] != temp[index][2]:
            with open(temp[i-1][:3]+OutFileSlve[3:],'w') as myFile2:
                for line in temp[index:i]: myFile2.write(line)
            index = i
            x = True
    if not x:
        with open(temp[0][:3]+OutFileSlve[3:],'w') as myFile2:
            for line in temp: myFile2.write(line)
    if x:
        with open(temp[-1][:3]+OutFileSlve[3:],'w') as myFile2:
            for line in temp[index:len(temp)]: myFile2.write(line)
        
    with open(OutFileMstr,'w') as myFile1:
        myFile1.write(mstrD)

if __name__=='__main__':

    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument("filename", help = "input filename to process, can be master or srvt csv type" )
    args = parser.parse_args()
    
    if args.filename is None:
        print('Input filename not specified!')
        sys.exit()

    lines = openFile(args.filename)
    if args.filename[0] == 'm':
        OutFileSlve =  "D01_master_data.txt"
        OutFileMstr =  "master_data.txt"
    else:
        OutFileSlve =  "D01_servant_LoRa_data.txt"
        OutFileMstr =  "D01_servant_1s_data.txt"
    
    sort(lines,OutFileSlve, OutFileMstr)
