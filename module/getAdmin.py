import ctypes, sys

class ExecuteAsAdmin:
    def __init__(self) -> None:
        self.isAdmin()
        self.getAdmin()
    
    def isAdmin(self):
        try:
            return ctypes.windll.shell32.IsUserAdmin()
        except:
            return False
        
    def getAdmin(self):
        if not self.isAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)