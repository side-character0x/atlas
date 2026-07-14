import subprocess
import webbrowser

class Launch:
    def open(self,target,url=None):
        if target:
            try:
                if url is None:
                    subprocess.Popen(target)
                else:
                    subprocess.Popen([target,url])
                return Launchresult(success=True,error=None)
            except FileNotFoundError:
                pass
        return Launchresult(success=False,error="File not found!")
    def search(self,url):
        if url:
            webbrowser.open(url)
            return Launchresult(success=True,error=None)
        else:
            return Launchresult(success=False,error="Url not found!")
    def system_cmd(self,action):
        if action=="shutdown":
            subprocess.Popen(["shutdown","/s","/t","2"])
        elif action=="restart":
            subprocess.Popen(["shutdown","/r","/t","2"])
        elif action=="sleep":
            subprocess.Popen(["rundll32.exe","powrprof.dll,SetSuspendState","0,1,0"])
class Launchresult:
    def __init__(self,success,error):
        self.success=success
        self.error=error