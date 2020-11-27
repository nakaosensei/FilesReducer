import subprocess
from os import listdir, mkdir, rmdir, rename

def uploadToGitHub(filePath, inputRange):
    dirfiles = listdir(path)
    dirfiles.sort()
    index = 0
    while(index < len(dirfiles)):
        toAdd = []
        for i in range(0, inputRange):
            toAdd.append(dirfiles[index])
            index = index + 1
        priint(toAdd)
        print('\n')


