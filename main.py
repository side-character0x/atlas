from interface import Interface
from router import Route
from action import Launch
from voice import Voice
import threading
class Main:
    def __init__(self):
        self.route=Route()
        self.interface=Interface(self.route)
        self.launch=Launch()
        self.voice=Voice(self.run)
        self.voice_thread = threading.Thread(
            target=self.voice.audio_detection,
            daemon=True
                                            )
        self.initiate_thread()
    def initiate_thread(self):
        self.voice_thread.start()
    def exit_handle(self,cmd):
        if cmd.lower()=="exit":
            return True
        else:
            return False
    def run(self,mode="keyboard"):
        if mode=="keyboard":
            self.keyboard_input()
        elif mode=="voice":
            while True:
                cmd=self.voice.voice_cmd()
                if not cmd:
                    self.voice.error_return("didn't receive any command")
                    continue
                response=self.home(cmd)
                if not response:
                    self.voice.error_return("received invalid command")
                else:
                    return
    def keyboard_input(self):
        while True:
            self.interface.exit_response()
            cmd=self.interface.query()
            if not cmd:
                self.interface.error_handle("Empty command!")
                continue
            response=self.exit_handle(cmd)
            if response:
                return
            self.home(cmd)
    def home(self,cmd):
        action,resource=self.route.evaluate(cmd)
        if action=="open":
            result=self.launch.open(resource)
        elif action=="search":
            result=self.launch.search(resource)
        elif action=='create':
            workspace_resources=self.interface.workspace_query()
            self.route.create_guide(resource,workspace_resources)
            return
        elif action=="load":
            for index,data_list in enumerate(resource):
                for data in data_list:
                    if index==0:
                        self.launch.open(data)
                    elif index==1:
                        self.launch.search(data)
                    elif index==2:
                        self.launch.open(data[0],url=data[1])
            return
        elif action=="view":
            if not resource:
                self.interface.error_handle("Workspace doesnot exist.")
                return
            self.interface.show_resources(resource)
            choice=self.interface.choice_query()
            if not choice:
                return
            symbols=self.interface.delete_query()
            self.route.delete_divert(symbols)
            return
        elif action=="system":
            self.launch.system_cmd(resource)
            return
        else:
            self.interface.error_handle("Invalid command!")
            return False
        if not result.success:
            self.interface.error_handle(result.error)
        else:
            return True
    

Main().run()