import os
from colorama import Fore, Style
import inspect
import clr
from init import *


def is_relevant(attribute):
    if ("method" in str(attribute[1])) and (not str(attribute[0]).startswith('__')): 
        return True
    else: 
        return False
    
def getModuleDocumentation(norconsultModule):
    """

    Args:
        norconsultModule (object): c# namespace of module imported from Norconsult
        Options: 
            - Norconsult.PI.APIConnect.Analysis
            - Norconsult.PI.APIConnect.Modelling
            - FEMDesign

    """
    
    for module in list(norconsultModule.__dict__.keys()): 
        if not module.startswith('__'):
            print()
            print(Fore.CYAN + module)
            try: 
                members = inspect.getmembers(globals()[module])
            except: 
                print(Fore.RED + "Cannot fetch methods for module: " + str(module))
                pass
                members = []
                
            for method in members:
                if is_relevant(method):
                    method_doc = inspect.getdoc(method[1])
                    func_with_args = method_doc.split(' ', maxsplit = 1)[1]
                    function_name = func_with_args.split('(')[0]
                    input_args = "(" + func_with_args.split('(')[1]
                    return_value = method_doc.split(' ', maxsplit = 1)[0].split('.')[-1].strip(']')
                    print(Fore.MAGENTA + " Method: " + function_name)
                    print(Fore.BLUE + " - Input arguments: " + input_args)
                    print(Fore.GREEN + " - Returns: " + return_value)
            print()


getModuleDocumentation(Norconsult.PI.APIConnect.Analysis)