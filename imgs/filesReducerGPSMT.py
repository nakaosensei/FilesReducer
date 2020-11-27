from os import listdir, mkdir, rmdir, rename
from os.path import isfile, join
import shutil
from GPSPhoto import gpsphoto
import geopy.distance
from pathlib import Path
import tkinter as tk
from ArrayUtils import splitArrayInNChunks
import threading
import asyncio
import time

postLat = 0
posLong = 1
classPosDotRange=3

def mountLatLongClass(latitude,longitude):
    latStr = str(latitude)
    splitDotLat = latStr.split('.')
    latPart = splitDotLat[0]+'.'+splitDotLat[1][0:classPosDotRange]

    longStr = str(longitude)
    splitDotLong = longStr.split('.')
    lotPart = splitDotLong[0]+'.'+splitDotLong[1][0:classPosDotRange]
    return latPart+'|'+lotPart

def loadPictureOnDict(picture, picturesDict, latLongDict, path):
    print('Will read GPS data from picture '+picture)
    innerPath = path / picture
    data = gpsphoto.getGPSData(innerPath.as_posix())
    picturesDict[picture] = (data['Latitude'],data['Longitude'])
    latLongDict[str( (data['Latitude'],data['Longitude']) )] = picture

def reduceConjunt(path, picturesDict, namesDict, distancesDict, orderedFiles, latLongClass, inputRange, rejecteds):
    
    print("Will save files")
    savedSequence = 0

    pivot = orderedFiles[0]
    pivotSplit = pivot.split('.')
    strSavedSequence = str(savedSequence) + '.' + pivotSplit[len(pivotSplit) - 1]
    print("Will save " + strSavedSequence)
    namesDict[strSavedSequence] = pivot
    shutil.copyfile(path / pivot, path / 'resultsFileReducer' / strSavedSequence)
    llclass = mountLatLongClass(picturesDict[pivot][postLat], picturesDict[pivot][posLong])
    if llclass in latLongClass:
        latLongClass[llclass].append(pivot)
    else:
        latLongClass[llclass] = [pivot]
    
    savedSequence += 1
    for i in range(1, len(orderedFiles)):
        distance = geopy.distance.distance(picturesDict[pivot], picturesDict[orderedFiles[i]]).m
        if distance >= inputRange:
            llclass = mountLatLongClass(picturesDict[orderedFiles[i]][postLat],picturesDict[orderedFiles[i]][posLong])
            closeToClassmate = False
            if llclass in latLongClass:
                onSameClass = latLongClass[llclass]                
                for classMate in onSameClass:
                    distance = geopy.distance.distance(picturesDict[classMate], picturesDict[orderedFiles[i]]).m
                    if distance <= inputRange:
                        closeToClassmate = True
                        rejecteds[orderedFiles[i]] = "distance:"+str(distance)+' | cause:classmate | comparedTo:'+classMate+' | class:'+llclass
            if closeToClassmate == False:
                pivot = orderedFiles[i]
                pivotSplit = pivot.split('.')
                strSavedSequence = str(savedSequence) + '.' + pivotSplit[len(pivotSplit) - 1]
                print("Will save " + strSavedSequence)
                namesDict[strSavedSequence] = pivot
                oldStrSavedSequence = str(savedSequence - 1) + '.' + pivotSplit[len(pivotSplit) - 1]
                distancesDict[oldStrSavedSequence + '-' + strSavedSequence] = distance
                shutil.copyfile(path / pivot, path / 'resultsFileReducer' / strSavedSequence)

                llclass = mountLatLongClass(picturesDict[pivot][postLat], picturesDict[pivot][posLong])
                if llclass in latLongClass:
                    latLongClass[llclass].append(pivot)
                else:
                    latLongClass[llclass] = [pivot]
                savedSequence += 1
        else:
            llclass = mountLatLongClass(picturesDict[orderedFiles[i]][postLat],picturesDict[orderedFiles[i]][posLong])
            rejecteds[orderedFiles[i]] = "distance:"+str(distance)+' | cause:pivot | comparedTo:'+pivot+' | class:'+llclass    
    print("Files saved")


def loadDict(dirfiles, picturesDict, latLongDict,path):
    print('Thread started')
    for picture in dirfiles:
        if isfile(  path / picture):
            loadPictureOnDict(picture, picturesDict, latLongDict, path)
    print('Thread finished')

def orderPictures(dirFiles):
    classesMaps = {}
    for file in dirFiles:
        if file!='resultsFileReducer':
            split = file.split('(')
            classe = split[0]
            if classe not in classesMaps:
                classesMaps[classe]={}
            splitDot = file.split('.')
            splitUnderline = splitDot[0].split('_')            
            sequence = int(splitUnderline[len(splitUnderline)-1])
            classesMaps[classe][sequence] = file
    
    arrayOrderedClassesMaps = {}
    for classe in classesMaps:
        sequences = list(classesMaps[classe].keys())
        sequences.sort()
        arrayOrderedClassesMaps[classe] = []
        for seq in sequences:            
            arrayOrderedClassesMaps[classe].append(classesMaps[classe][seq])

    orderedPictures = []
    orderedClasses = list(arrayOrderedClassesMaps.keys())
    orderedClasses.sort()
    for classe in orderedClasses:
        for picture in arrayOrderedClassesMaps[classe]:
            orderedPictures.append(picture)
    
    return orderedPictures


def renameFiles(path):    
    print("Will read files from dir...")
    dirFiles = listdir(path)
    for f in dirFiles:
        if '(' not in f and ')' not in f:
            parts = f.split('_')
            new = parts[0]+'(1)'
            for i in range(1, len(parts)):
                new+='_'+parts[i]            
            rename(path / f, path / new)
    '''
    print("Will read files from dir...")
    dirFiles = listdir(path)
    for f in dirFiles:
        if '(1)' in f:
            parts = f.split('(1)')
            new = parts[0]+' (1)'+parts[1]                        
            rename(path / f, path / new)
    '''
#Range = 4, a cada 4 arquivos salva só o ultimo
def reduceFiles(dirPath, inputRange):
    starttime = time.time()
    asyncio.set_event_loop(asyncio.new_event_loop())
    path = Path(dirPath)
    try:
        shutil.rmtree(path / 'resultsFileReducer')
        worked = 1        
    except:
        print('')

    renameFiles(path)
    print("Will read files from dir...")
    dirfiles = listdir(path)
    print(len(dirfiles))
    print("Finish")
    print(len(dirfiles))

    
    
    return Trueworked = 0
    while worked == 0:        
        dirSequenceMap = {} #Key:fileName Value:FilenameSequence(int)
        dirIntSequenceMap = {} #Key:intIndes Value:fileName
        rejecteds = {} #Key:filename | comparedTo:BaseCompare|Distance|classmate
        picturesDict = {}  # Key:pictureName Value (latitude, longitude)
        latLongDict = {}   # Key:(lat,Long) Value pictureName
        namesDict = {}  # Key:newSequenceName Value:oldFileName
        distancesDict = {}     # Key:newSequenceName1-newSequenceName2 Value:distance

        # Key:LatClass+|+LongClass, latclass = before dot + the first 4 chars of lat after dot, longClass = before dot + the first 4 chars of long after dot
        # Value: Array of filesNames
        latLongClass = {}

        try:
            mkdir(path / 'resultsFileReducer')
            worked = 1
        except:
            print('erro ao criar diretorio')
        
      
        '''
        print("Will load files")
        if len(dirfiles)>=10:
            splits = splitArrayInNChunks(dirfiles, 10)
            workers = []
            for splt in splits:
                print(len(splt))
                if len(splt)>0:
                    t = threading.Thread(target=loadDict,args=(splt, picturesDict, latLongDict, path))
                    t.start()
                    workers.append(t)
            for w in workers:
                w.join()
        else:
            for picture in dirfiles:
                if isfile(path / picture):
                    loadPictureOnDict(picture, picturesDict, latLongDict, path)'''

        print("Loaded all files")
        
        
        

        print(len(picturesDict))

        reduceConjunt(path, picturesDict, namesDict, distancesDict, orderedFiles, latLongClass, inputRange, rejecteds)

        print("Save finished")
        print("time elapsed: {:.2f}s".format(time.time()-starttime))

        f = open(path / 'resultsFileReducer' / 'distances.txt', 'w')
        f.write('\r\nDistances:\r\n')
        for pair in distancesDict:
            f.write(pair + ": " + str(distancesDict[pair]) + '\n')
        f.close()

        f = open(path / 'resultsFileReducer' / 'rejecteds.txt','w')
        for rejected in rejecteds:
            f.write(rejected+' - '+rejecteds[rejected]+"\n")
        f.close()        

        f = open(path / 'resultsFileReducer' / 'mapping.txt', 'w')
        f.write('\n\rnames:\r\n')
        for name in namesDict:
            f.write(name + " = " + namesDict[name] + '\n')
        f.close()


        f = open(path / 'resultsFileReducer' / 'latsLongs.txt', 'w')
        f.write('\n\rnames:\r\n')
        for name in namesDict:
            f.write(name + " - " + str(picturesDict[namesDict[name]]) + '\n')
        f.close()

        f = open(path / 'resultsFileReducer' / 'latsLongClasses.txt', 'w')
        f.write('\n\rclasses:\r\n')
        for clss in latLongClass:
            f.write(clss + " - " + str(latLongClass[clss]) + '\n')
        f.close()
        return True'''
    
