import os

def make():
    print("Creating OS folders in need! This may take a few seconds or minutes!")
    os.system('git clone https://github.com/WWEMGamer2/OS-Folders.git')
    os.system('cp ./OS-Folders/* ./')
    os.system('rm ./OS-Folders/*')
    i = input('[./OS/config.py] What is your OS name? ')
    print("Formatting...")
    os.system(f'mv ./OS ./{i}')
    i = input('[./OS/config.py] Where is your mandatory folder? ')
    for f in os.listdir('./'):
        if i == f:
            print("Found the required folder.")
            print("Formatting...")
        else: 
            print("Found no folder under the name specified.")
            if input('Would you like to create it? (y,n) ') == "y":
                os.mkdir(f'./OS/{i}')
    
    print(f"[!] The process was completed. You can now remove the make() function from {__name__}.py")