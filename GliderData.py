

# Created 14/06/2021
# @Author: Juraj Janekovic

import sys
import geopy.distance
from datetime import datetime
import time
import folium
from folium.plugins import MarkerCluster
import pandas as pd

perth_cords = [-31.984687, 115.835413]
myMap = folium.Map(location = perth_cords, zoom_start = 13)
tile = folium.TileLayer(
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
        ).add_to(myMap)

colours = {'D01':'blue','D02':'green','D03':'yellow','D04':'purple','D05':'orange',
               'D06':'pink','D07':'beige','D08':'red','D09':'lightgreen'}

def openFile(csv):
    with open(csv,'r', encoding = "ISO-8859-1") as myfile:
        lines = myfile.readlines()
    return lines

def sort(lines,OutFileSlve, OutFileMstr):
    points = []
    pointsD = []
    mstrD = ""
    mstrTemp = []
    temp = []
    m = True
    count = 10
    countr = 10
    for line in lines:
        if len(line) > 2:
            try:
                if line[0] == "D" and line[29] != '0' and (len(line.split(','))) == 8:
                    m = False
                    if count % 10 == 0:
                        pointsD.append([float(line.split(',')[5]),float(line.split(',')[4])])
                    if not isM:
                        colourD = colours.get(line[0:3])
                    temp.append(line)
                    count += 1
            except IndexError: continue
           
            else:
                try:
                    if line.split(',')[2] != '0.00000000' and line[0] == '2':
                        if countr % 10 == 0:
                            points.append([float(line.split(',')[3]),float(line.split(',')[2])])
                        mstrTemp.append(line)
                        mstrD += line
                        countr += 1
                except IndexError: continue

    prevs = points[0]
    for i in range (len(points)):
        if CalcDistance(prevs[0], prevs[1], points[i][0],points[i][1]) < 0.5:      
            folium.PolyLine([prevs,points[i]], color=colourD, weight=2.5, opacity=1).add_to(myMap)
        prevs = points[i]
    
    prevs = pointsD[0]
    for i in range (len(pointsD)):
        if CalcDistance(prevs[0], prevs[1], pointsD[i][0],pointsD[i][1]) < 0.5:      
            folium.PolyLine([prevs,pointsD[i]], color=colourD, weight=2.5, opacity=1).add_to(myMap)
        prevs = pointsD[i]
    
    for i in range (1,len(mstrTemp),60):
        l = mstrTemp[i-1].split(',')
        n = mstrTemp[i].split(',')
        speed = CalcSpeed(l[0]+', ' + l[1] + ', ' + l[3] + ', ' + l[2] + ', ' + l[4], n[0]+', ' + n[1] + ', ' + n[3] + ', ' + n[2] + ', ' + n[4])
        if isM:
            addPoint(mstrTemp[0],'black',True,"Mystery")
            addPoint(mstrTemp[i],'black',True,speed)
        else: 
            addPoint(mstrTemp[0],colourD,True,"Mystery")
            addPoint(mstrTemp[i],colourD,True,speed)
        
        
                
    temp.sort()
    index = 0
    x = False
    for i in range (1,len(temp)):
        if temp[i][:3] != temp[index][:3]:
            with open(temp[i-1][:3]+OutFileSlve[3:],'w') as myFile2:
                previous = temp[index-1]
                for line in temp[index:i]:
                    lineOriginal = line
                    previous = previous.split(',')
                    line = line.split(',')
                    speed = CalcSpeed(previous[2]+', '+previous[3]+', '+previous[4]+', '+previous[5],line[2]+', '+line[3]+', '+line[4]+', '+line[5])
                    
                    addPoint(lineOriginal,colours.get(temp[i][:3]),False,speed)
                    myFile2.write(lineOriginal)
                    previous = lineOriginal
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

    
def addPoint(line,colour,x,speed):
    if x:
        
        coordinate = [float(line.split(',')[3]), float(line.split(',')[2])]
                                    
        folium.CircleMarker(
        radius = 1.5,
        location=coordinate,
        color=colour,
        popup= "Date " + line.split(',')[0] + "\n" + "Time " + line.split(',')[1] + "\n" + "Speed " + str(speed),
        fill=True,
        fill_color= colour,
        ).add_to(myMap)

    else:
        try:
            if (len(line.split(','))) == 8: 
                coordinate = [float(line.split(',')[4]),float(line.split(',')[5])]
                popup1=line.split(',')[:4]
                
                folium.CircleMarker(
                radius = 1.5,
                location=coordinate,
                color = colour,
                popup = "Slave " + popup1[0] + "\n" + "Date " + popup1[2] + "\n" + "Time " + popup1[3] + "Speed " + str(speed)
                ).add_to(myMap)
            
        except ValueError:
            return


def CalcDistance(lat,long, lat2, long2):
    coords_1 = (lat, long)
    coords_2 = (lat2, long2)
        
    dist = geopy.distance.distance(coords_1, coords_2).km
    return round(dist,5)

def CalcSpeed(line,line2):
    try:
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(line.split(',')[0]+ " " + line.split(',')[1], fmt)
        d2 = datetime.strptime(line2.split(',')[0]+ " " + line2.split(',')[1], fmt)
        diff = d2 -d1
        diff_hours = (diff.days * 24) + (diff.seconds/3600)
        
        dist = CalcDistance(float(line.split(',')[2]), float(line.split(',')[3]), float(line2.split(',')[2]), float(line2.split(',')[3]))
    
        ans = dist/diff_hours
        return round(ans,0)

    except ValueError:
        return


if len(sys.argv) >= 2:
    for i in range (1,len(sys.argv)):
        filename = sys.argv[i]  
        if filename[0] == 'm':
            isM = True
        else: isM = False
        lines = openFile(filename)
        if filename[0] == 'm':
            isM = True
            OutFileSlve =  "D01_master_data.txt"
            OutFileMstr =  "master_data.txt"
        else:
            OutFileSlve =  "D01_servant_LoRa_data.txt"
            OutFileMstr =  "D01_servant_1s_data.txt"
        
        sort(lines,OutFileSlve, OutFileMstr)
myMap.save('map.html')
    
    
            


