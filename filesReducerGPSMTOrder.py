from os import listdir, mkdir, rmdir
from os.path import isfile, join
import shutil
from GPSPhoto import gpsphoto
import geopy.distance
from pathlib import Path
import tkinter as tk
from ArrayUtils import splitArrayInNChunks
import threading
import mergeSort as mSort
import asyncio
import time


def loadPictureOnDict(picture, picturesDict, latLongDict, path):
    innerPath = path / picture
    data = gpsphoto.getGPSData(innerPath.as_posix())
    picturesDict[picture] = (data['Latitude'],data['Longitude'])
    latLongDict[str( (data['Latitude'],data['Longitude']) )] = picture

def reduceConjunt(path, picturesDict, latLongDict, orderedLatLong, namesDict, distancesDict,inputRange):
    print("Will save files")
    savedSequence = 0
    pivot = latLongDict[str(tuple(orderedLatLong[0]))]
    pivotSplit = pivot.split('.')
    strSavedSequence = str(savedSequence) +'.'+pivotSplit[len(pivotSplit)-1]
    print("Will save "+strSavedSequence)
    namesDict[strSavedSequence]=pivot
    shutil.copyfile(path / pivot, path / 'resultsFileReducer' / strSavedSequence)
    savedSequence+=1
    for i in range(1, len(orderedLatLong)):
        distance = geopy.distance.distance(picturesDict[pivot], orderedLatLong[i]  ).m
        if distance >= inputRange:
            pivot = latLongDict[str(tuple(orderedLatLong[i]))]
            pivotSplit = pivot.split('.')
            strSavedSequence = str(savedSequence) + '.' + pivotSplit[len(pivotSplit)-1]
            print("Will save " + strSavedSequence)
            oldStrSavedSequence = str(savedSequence-1)+ '.' +pivotSplit[len(pivotSplit)-1]
            namesDict[strSavedSequence] = pivot
            distancesDict[oldStrSavedSequence+'-'+strSavedSequence] = distance
            shutil.copyfile(path / pivot, path / 'resultsFileReducer' / strSavedSequence)
            savedSequence += 1
    print("Files saved")

def loadDict(dirfiles, picturesDict, latLongDict,path):
    for picture in dirfiles:
        if isfile(  path / picture):
            loadPictureOnDict(picture, picturesDict, latLongDict, path)

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
            
    worked = 0
    while worked == 0:
        try:
            mkdir(path / 'resultsFileReducer')
            worked = 1
        except:
            print('erro ao criar diretorio')

    print("Will read files from dir...")
    dirfiles = listdir(path)
    print(len(dirfiles))
    print("Finish")
    print(len(dirfiles))
    dirfiles.sort()
    picturesDict = {}  # Key:pictureName Value (latitude, longitude)
    latLongDict = {}   # Key:(lat,Long) Value pictureName
    namesDict = {}  # Key:newSequenceName Value:oldFileName
    distancesDict = {}     # Key:newSequenceName1-newSequenceName2 Value:distance

    print("Will load files")
    if len(dirfiles)>=100:
        splits = splitArrayInNChunks(dirfiles, 100)
        workers = []
        for splt in splits:
            if len(splt)>0:
                t = threading.Thread(target=loadDict,args=(splt, picturesDict, latLongDict, path))
                t.start()
                workers.append(t)
        for w in workers:
            w.join()
    else:
        for picture in dirfiles:
            if isfile(path / picture):
                loadPictureOnDict(picture, picturesDict, latLongDict, path)

    orderedLatLong = list(picturesDict.values())
    mSort.merge_sort(orderedLatLong)

    print('done merge sort')

    f = open(path / 'resultsFileReducer' / 'orderLatLong.txt','w')
    f.write("Sequence by lat long \r\n")
    for latLong in orderedLatLong:
        f.write(str(latLong)+"\r\n")

    f.write('\n\rSequence fileNames:\r\n')
    for latLong in orderedLatLong:
        f.write(latLongDict[str(tuple(latLong))]+"\r\n")
    f.close()

    print("Loaded all files")

    print(len(picturesDict))
    print(orderedLatLong)
    reduceConjunt(path, picturesDict, latLongDict, orderedLatLong, namesDict, distancesDict, inputRange)

    print("Save finished")
    print("time elapsed: {:.2f}s".format(time.time()-starttime))

    f = open(path / 'resultsFileReducer' / 'distances.txt', 'w')
    f.write('\r\nDistances:\r\n')
    for pair in distancesDict:
        f.write(pair + ": " + str(distancesDict[pair]) + '\r\n')
    f.close()

    f = open(path / 'resultsFileReducer' / 'mapping.txt', 'w')
    f.write('\n\rnames:\r\n')
    for name in namesDict:
        f.write(name + " = " + namesDict[name] + '\r\n')
    f.close()
    return True
