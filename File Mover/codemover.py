import os
import shutil #Used to delete a folder recursively

toGoFolder = "C:\\Users\\cezar\\Desktop\\Algo\\CodeFileOnly"
toComeFolder = "C:\\Users\\cezar\\Desktop\\Algo"

subfolders = ["Infoarena","pbinfo"]

def moveFiles(folder):
    destination = os.path.join(toGoFolder,folder) #Where do we get the codes from.
    source = os.path.join(toComeFolder,folder)  #Where the codes go.
    
    for subFolder in os.listdir(source): #Check every project folder from the source
        for file in os.listdir(os.path.join(source,subFolder)): #Check every file of the project
            if getExtension(file)=='.cpp':  #If it is .cpp file, which we are interested in, move it
                filePath = os.path.join(source,subFolder,file)
                destFile = os.path.join(destination,f"{subFolder}.cpp")
                if not os.path.exists(destFile):    #Check if the files doesn't exists already (kinda redundant)
                    os.rename(filePath,destFile)    #Move the file
        shutil.rmtree(os.path.join(source,subFolder))   #Delete the project directory.
                
        
def getExtension(file): #Get the extension of a file
    name,extension = os.path.splitext(file)
    return extension

#Check if folder exists, otherwise, create it
def checkFolders():
    if not os.path.exists(toGoFolder):
        os.mkdir(toGoFolder)
        for tempFolder in subfolders:
            newFolder = os.path.join(toGoFolder,tempFolder)
            os.mkdir(newFolder)


def main():
    checkFolders()
    
    for subFolder in subfolders:
        moveFiles(subFolder)
        
main()