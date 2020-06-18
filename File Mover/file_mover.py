import os
import time

toGoFolder = "C:\\Users\\cezar\\Desktop\\to_go"
toComeFolder = "C:\\Users\\cezar\\Desktop\\to_come"

subfolders = ["c++", "txt", "py", "misc"]


def move_file(fileName, extension):
    
    moved = 0
    filePath = os.path.join(toGoFolder, fileName)
    for tempExt in subfolders:
        if extension == f".{tempExt}":
            
            tempFolder = os.path.join(toComeFolder, tempExt)
            tempFolder = os.path.join(tempFolder, fileName)
            os.rename(filePath, tempFolder)
            
            moved = 1
            break
            
    if moved == 0:
        tempFolder = os.path.join(toComeFolder, "misc")
        tempFolder = os.path.join(tempFolder, fileName)
        os.rename(filePath, tempFolder)
    
    
def getFileExtension(fileName):
    name, extension = os.path.splitext(fileName)
    return extension


def checkFolders():
    if not os.path.exists(toComeFolder):
        os.mkdir(toComeFolder)
        for tempExt in subfolders:
            os.mkdir(os.path.join(toComeFolder, tempExt))
            
    if not os.path.exists(toGoFolder):
        os.mkdir(toGoFolder)


def main():
    # First, check if the 2 folders already exists. Otherwise, create them
    checkFolders()

    # When there is something in the folder, move it in its corresponding destination.
    while True:
        if len(os.listdir(toGoFolder)) > 0:
            for file in os.listdir(toGoFolder):
                fileExt = getFileExtension(file)
                move_file(file, fileExt)
        time.sleep(10)


main()
