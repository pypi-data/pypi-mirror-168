import os
import time

ivar = "OS-Folders"

def make():
    print("Creating OS folders in need! This may take a few seconds or minutes!")
    os.system('git clone https://github.com/WWEMGamer2/OS-Folders.git')
    i = input('[./OS/config.py] What is your OS name? (provide . to be hidden) ')
    print("Formatting...")
    ivar = i
    os.system(f'mv ./OS-Folders ./{i}')
    i = input('[./OS/config.py] Where is your mandatory folder? ')
    for f in os.listdir(f'./{i}'):
        if i == f:
            print("Found the required folder.")
            print("Formatting...")
        else: 
            print("Found no folder under the name specified.")
            if input('Would you like to create it? (y,n) ') == "y":
                os.mkdir(f'./OS/{i}')
    
    print(f"[!] The process was completed. You can now remove the make() function from {__name__}.py")

def makes(ivar2):
    #print("Creating OS folders in need! This may take a few seconds or minutes!")
    #os.system('git clone https://github.com/WWEMGamer2/OS-Folders.git')
    i = input('[./OS/config.py] Where is your mandatory folder? ')
    for f in os.listdir(f'./'):
        if i == f:
            print("Found the required folder.")
            print("Formatting...")
            print("Put settings into PYOS-MANAGER.properties")
            print(f"[!] The process was completed. Please add the 'osfolder' attribute to the run() function.")
            return
        
    print("Found no folder under the name specified.")
    if input('Would you like to create it? (y,n) ') == "y":
        os.mkdir(f'./{ivar2}/{i}')
        print(f"[!] The process was completed. Please add the 'osfolder' attribute to the run() function.")
        return

def run(osfolder=None):
    if osfolder != None:
        print("[PYOS-MANAGER] Running OS with PyOS.core.modules.oracle")
        time.sleep(1)
        try:
            os.system(f'python3 {osfolder}/run.py')
        except Exception:
            print("[PYOS-MANAGER] Failed to run the OS with oracle: CODE 400")
    else: print(f"[PYOS-MANAGER] OS folder has not been identified. Identified as: unknown"); i = input('[!] Run folder? '); ivar = i; makes(ivar); 