from os import listdir, mkdir, rmdir
from os.path import isfile, join
import shutil
from GPSPhoto import gpsphoto
import geopy.distance
from pathlib import Path
import tkinter as tk
from ArrayUtils import splitDictEqually, splitArrayInNChunks
from multiprocessing import Process
from tkinter import filedialog
import threading
import asyncio
import time
DISTANCIA_METROS = 10


def loadPictureOnDict(picture, picturesDict, latLongDict, path):
    innerPath = path / picture
    data = gpsphoto.getGPSData(innerPath.as_posix())
    picturesDict[picture] = (data['Latitude'],data['Longitude'])
    latLongDict[str( (data['Latitude'],data['Longitude']) )] = picture

def reduceConjunt(path, filesDict,picturesDict, inputRange):    
    print("Will save files")
    listKeys = list(filesDict)
    pivot = listKeys[0]
    print("Will save "+pivot)
    shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    for i in range(1, len(listKeys)):
        distance = geopy.distance.distance(picturesDict[pivot], picturesDict[listKeys[i]]).m
        if distance >= inputRange:            
            pivot = listKeys[i]
            print("Will save "+pivot)
            shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    print("Files saved")

def reduceConjunt2(path, filesDict,picturesDict, latLongDict, orderedLatLong, inputRange):    
    print("Will save files")
    listKeys = list(filesDict)
    saveds = 0
    pivot = latLongDict[orderedLatLong[0]]
    print("Will save "+pivot)
    shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    for i in range(1, len(orderedLatLong)):
        distance = geopy.distance.distance(picturesDict[pivot], picturesDict[latLongDict[orderedLatLong[i]]]  ).m
        if distance >= inputRange:            
            pivot = latLongDict[orderedLatLong[i]]
            print(pivot)
            print("Will save "+pivot)
            shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    print("Files saved")


def loadDict(dirfiles, picturesDict, latLongDict,path):
    for picture in dirfiles:
        if isfile(  path / picture):
            loadPictureOnDict(picture, picturesDict, path)

#Range = 4, a cada 4 arquivos salva só o ultimo
def reduceFiles(dirPath, inputRange):
    starttime = time.time()
    asyncio.set_event_loop(asyncio.new_event_loop())
    path = Path(dirPath)
    try:
        shutil.rmtree(path / 'resultsFileReducer')
    except:
        print('')
    mkdir(path / 'resultsFileReducer')
    print("Will read files from dir...")
    dirfiles = listdir(path)
    print(len(dirfiles))
    print("Finish")
    print(len(dirfiles))
    dirfiles.sort()    
    picturesDict = {} # Key:pictureName Value (latitude, longitude)
    latLongDict = {}  # Key:(lat,Long) Value pictureName

    print("Will load files")

    for picture in dirfiles:
        if isfile(path / picture):
            loadPictureOnDict(picture, picturesDict, latLongDict, path)
    
    orderedLatLong = list(latLongDict.keys())
    orderedLatLong.sort()


    print("Loaded all files")
    print(len(picturesDict))



    reduceConjunt2(path, picturesDict, picturesDict, latLongDict, orderedLatLong, inputRange)

    print("Save finished")
    print("time elapsed: {:.2f}s".format(time.time()-starttime))
    return True    

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    reduceFiles('samples/', DISTANCIA_METROS)


