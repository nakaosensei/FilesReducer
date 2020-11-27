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


def loadPictureOnDict(picture, picturesDict, path, mutex):
    innerPath = path / picture
    data = gpsphoto.getGPSData(innerPath.as_posix())
    mutex.acquire()
    picturesDict[picture] = (data['Latitude'],data['Longitude'])
    mutex.release()

def reduceConjunt(path, filesDict,picturesDict, inputRange):    
    print("Will save files")
    listKeys = list(filesDict)
    pivot = listKeys[0]
    print("Will save "+pivot)
    shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    for i in range(1, len(listKeys)):
        distance = geopy.distance.vincenty(picturesDict[pivot], picturesDict[listKeys[i]]).m
        if distance >= inputRange:            
            pivot = listKeys[i]
            print("Will save "+pivot)
            shutil.copyfile(path / pivot, path / 'resultsFileReducer' / pivot)
    print("Files saved")


def loadDict(dirfiles, picturesDict, path,mutex):
    for picture in dirfiles:
        if isfile(  path / picture):
            loadPictureOnDict(picture, picturesDict, path, mutex)

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
    mutex = asyncio.Semaphore(1)
    print("Will load files")          
    if len(dirfiles)>=6:        
        splits = splitArrayInNChunks(dirfiles, 100)
        workers = []
        for splt in splits:
            print(len(splt))
            t = threading.Thread(target=loadDict,args=(splt, picturesDict, path,mutex,))
            t.start()
            workers.append(t)
        for w in workers:
            w.join()
    else:
        for picture in dirfiles:
            if isfile(path / picture):
                loadPictureOnDict(picture, picturesDict, path, mutex)
    print("Loaded all files")
    print(len(picturesDict))
    
    chunks = splitDictEqually(picturesDict, 2 )
    groups = []
       
    for chk in chunks:        
        p = Process(target=reduceConjunt, args=(path, chk.copy(), picturesDict.copy(), inputRange))
        p.start()
        groups.append(p)

    for grp in groups:
        grp.join()
    print("Save finished")
    print("time elapsed: {:.2f}s".format(time.time()-starttime))
    return True
    

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    reduceFiles('samples/', DISTANCIA_METROS)


