from os import listdir, mkdir, rmdir
from os.path import isfile, join
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


QUANTIDADE_DE_ARQUIVOS = 4


#Range = 4, a cada 4 arquivos salva só o ultimo
def reduceFiles(dirPath, inputRange):
    path =  Path(dirPath)
    try:
        shutil.rmtree(path / 'resultsFileReducer')
    except:
        print('Dir nao existe')
    mkdir(path / 'resultsFileReducer')
    rangeCopy = inputRange
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles.sort()
    filesToSave = {}
    for i in range(0, len(onlyfiles)):
        if i + 1 == rangeCopy:
            shutil.copyfile(path / onlyfiles[i],path / 'resultsFileReducer' / onlyfiles[i])
            filesToSave[onlyfiles[i]]=i
            rangeCopy += inputRange
    return filesToSave

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    try:
        file_path = filedialog.askdirectory()
        print(reduceFiles(file_path, QUANTIDADE_DE_ARQUIVOS))
    except:
        print("failed")


