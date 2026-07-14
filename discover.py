import winreg
from pathlib import Path
from win32com.client import Dispatch
from atlasreg import Database
import shutil
import requests

class Paths:
    def __init__(self):
        self.reg=Database()
    def store_data(self,name,path,type="path",resource_type=None,browsers=None):
        if type=="path":
            self.reg.store_path(name,path)
        elif type=="workspace":
            for i in range(len(path)):
                responce=self.reg.check_workspace(path[i])
                if not responce:
                    self.reg.store_workspace(name,resources=path[i],type=resource_type[i],browser=browsers[i])
    def windowsreg(self,target):
        try:
            exe=target+".exe"
            app_paths=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
            required_key=winreg.OpenKey(app_paths,exe)
            path,_=winreg.QueryValueEx(required_key,"")
            self.store_data(target,path)
            return path
        except FileNotFoundError:
            return False
    def start_menu(self,target):
        folder=Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
        for file in folder.rglob("*.lnk"):
            if file.stem.lower()==target:
                return file
        folder=Path(r"C:\Users\prett\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
        for file in folder.rglob("*.lnk"):
            if file.stem.lower()==target:
                return file
        return False
    def find_path(self,target):
        shortcut=self.start_menu(target)
        if not shortcut:
            return False
        shell = Dispatch("WScript.Shell")
        shortcut_obj = shell.CreateShortcut(str(shortcut))
        path= shortcut_obj.targetpath
        self.store_data(target,path)
        return path
    def atlasreg(self,target):
        path=self.reg.check_path(target)
        return path
    def winpath_validity(self,target):
        responce=shutil.which(target)
        return responce
    def url_validity(self,target):
        try:
            responce=requests.get(target)
            if responce.status_code==200:
                return True
            else:
                return False
        except requests.exceptions.MissingSchema:
            return False
    def convey_resources(self,workspace,use="load"):
        if use=="load":
            resources=self.reg.load_workspace(workspace)
            return resources
        elif use=="delete":
            for resource in workspace:
                self.reg.delete_workspace(int(resource))



         