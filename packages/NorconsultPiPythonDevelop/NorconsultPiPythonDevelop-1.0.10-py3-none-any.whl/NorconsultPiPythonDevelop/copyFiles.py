
import os 
from serverPaths import getServerPaths
import shutil

def copyAllFiles(): 
    serverPaths = getServerPaths()

    destinationFolder = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelop\\"
    destinationFolderAuth =  "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelopAuth\\"
    destinationFolderDocumentation =  "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelopDocumentation\\"


    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
        
    if not os.path.exists(destinationFolderAuth):
        os.makedirs(destinationFolderAuth)

    if not os.path.exists(destinationFolderAuth):
        os.makedirs(destinationFolderDocumentation)
        
    analysisPath = serverPaths["Analysis"]
    modellingPath = serverPaths["Modelling"]
    modelBuilderFEMPath = serverPaths['ModelBuilder_FEM']
    modelBuilderRobotPath = serverPaths["ModelBuilder_Robot"]
    auth_python_Path = serverPaths["auth_python"]
    documentationPath = serverPaths["documentation"]

    filesToCopyAnalysis = os.listdir(analysisPath)
    filesToCopyModelling = os.listdir(modellingPath)
    filesToCopyFEM = os.listdir(modelBuilderFEMPath)
    filesToCopyRobot = os.listdir(modelBuilderRobotPath)
    filesToCopy_auth_python = os.listdir(auth_python_Path)
    filesToCopyDocumentation = os.listdir(documentationPath)

    for file in filesToCopyAnalysis: 
        if requiresUpdate(analysisPath + file, destinationFolder + file): 
            shutil.copyfile(analysisPath + file, destinationFolder + file)
            
    for file in filesToCopyModelling: 
        if requiresUpdate(modellingPath + file, destinationFolder + file): 
            shutil.copyfile(modellingPath + file, destinationFolder + file)

    for file in filesToCopyFEM: 
        if requiresUpdate(modelBuilderFEMPath + file, destinationFolder + file): 
            shutil.copyfile(modelBuilderFEMPath + file, destinationFolder + file)
            
    for file in filesToCopyRobot: 
        if requiresUpdate(modelBuilderRobotPath + file, destinationFolder + file): 
            shutil.copyfile(modelBuilderRobotPath + file, destinationFolder + file)
    
    for file in filesToCopy_auth_python:
        if requiresUpdate(auth_python_Path + file, destinationFolderAuth + file):
            shutil.copyfile(auth_python_Path + file, destinationFolderAuth + file)
    
    for file in filesToCopyDocumentation:
        if file.endswith(".html"): 
            if requiresUpdate(documentationPath + file, destinationFolderDocumentation + file):
                shutil.copyfile(documentationPath + file, destinationFolderDocumentation + file)
    

def requiresUpdate(serverFilePath, destFilePath):
    if not os.path.isfile(destFilePath): 
        return True 
    
    serverFilePathCreatedDate = os.path.getmtime(serverFilePath)
    destFilePathCreatedDate = os.path.getmtime(destFilePath)
    if serverFilePathCreatedDate >  destFilePathCreatedDate: 
        return True

    return False