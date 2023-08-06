import subprocess
import os
import clr
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from copyFiles import copyAllFiles
from generateDocs import getModuleDocumentation
#Copy All Files
copyAllFiles()

#Authentificate
authPath = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelop_auth\\PiPython.exe"
subprocess.check_call([authPath])

##Importing PI libraries and dependencies
referenceFolder = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelop"
modellingDllPath = referenceFolder + "\\APIClientModelling.dll" 
analysisDllPath = referenceFolder + "\\APIClientAnalysis.dll" 
commonDllPath = referenceFolder + "\\Norconsult.PI.Common.dll"
FEMmodelBuilderPath = referenceFolder + "\\ModelBuilder_FEM_Design.dll";
RobotModelBuilderPath = referenceFolder + "\\ModelBuilder_Robot.dll"

clr.AddReference(modellingDllPath)
clr.AddReference(analysisDllPath)
clr.AddReference(commonDllPath)
clr.AddReference(FEMmodelBuilderPath)
clr.AddReference(RobotModelBuilderPath)

#Imports 
import Norconsult.PI.APIConnect.Analysis as aapi 
import Norconsult.PI.Common.API.Models.Analysis as adto
import Norconsult.PI.APIConnect.Analysis.Extensions as aext
import Norconsult.PI.APIConnect.Helpers.Analysis as ahel

import Norconsult.PI.APIConnect.Modelling as mapi 
import Norconsult.PI.Common.API.Models.Modelling as mdto
import Norconsult.PI.APIConnect.Modelling.Extensions as mext
import Norconsult.PI.APIConnect.Helpers.Modelling as mhel

import FEMDesign as fem
import Robot as robot

#Apperently we have to import clr twice so add Norconsult namespace in clr
import clr
print("Welcome to PiPython!")
print("This is the develop version of our package, this means all request will be sent to our test database.")
print("If you need startup help, check the documentation file: " + str("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Norconsult\\NorconsultPiPythonDevelopDocumentation\\README.html"))


