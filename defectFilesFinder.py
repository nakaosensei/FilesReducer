import shutil
from os import listdir, mkdir, rmdir

def checkFilesInDirCanBeCopied(path):
    dirfiles = listdir(path)
    errorFiles = ""
    for fileOpen in dirfiles:
        if ('.jpg' in fileOpen or '.png' in fileOpen):
            try:
                shutil.copyfile(path / fileOpen, path / 'tmp'+fileOpen)
                os.remove(path / 'tmp'+fileOpen)
            except:
                errorFiles+=fileOpen+'\n'
    return errorFiles
    
