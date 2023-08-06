# This file is apart of the PyOS module. Editing this file may change your OS, but may break it. Please edit the file if you know what you are doing and take caution.

class Setup:
    class private:
        def __init__(self):
            self.authent = None

    def systemauthenticate(self): 
        self.private.authent = "authenticated"

    def AskQuestion(self, question):
        if self.private.authent == "authenticated":
            input(f'[?] {question}')
        else: print("* You don't have permission to run this. \n * This may been because you edited the files in the OS folder \nReset your OS by running the make() function.")
    
    def PrintStartupMessage(self, message):
        import time
        import os

        if self.private.authent == "authenticated":
            print(message)
            print("* Powered by PyOS")
            time.sleep(2)
            os.system('clear')
        else: print("* You don't have permission to run this. \n * This may been because you edited the files in the OS folder \nReset your OS by running the make() function.")
