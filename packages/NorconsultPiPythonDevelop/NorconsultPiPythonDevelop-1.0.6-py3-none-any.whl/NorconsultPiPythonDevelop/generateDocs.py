from colorama import Fore, Style
import inspect

def is_relevant(attributeName, attribute):
    if ("method" in str(attribute)) and (not str(attributeName).startswith('__')): 
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
    #for discpiline, bar, node etc
    for moduleName, module in inspect.getmembers(norconsultModule):
        if not moduleName.startswith('__'):
            print()
            print(Fore.CYAN + moduleName)
            
            try: 
                members = inspect.getmembers(module)
            except: 
                print(Fore.RED + "Cannot fetch methods for module: " + str(module))
                pass
                members = []
                
            for methodName, method in members:
                if is_relevant(methodName, method):
                    method_doc = inspect.getdoc(method)
                    func_with_args = method_doc.split(' ', maxsplit = 1)[1]
                    function_name = func_with_args.split('(')[0]
                    input_args = "(" + func_with_args.split('(')[1]
                    return_value = method_doc.split(' ', maxsplit = 1)[0].split('.')[-1].strip(']')
                    print(Fore.MAGENTA + " Method: " + function_name)
                    print(Fore.BLUE + " - Input arguments: " + input_args)
                    print(Fore.GREEN + " - Returns: " + return_value)
            print()


