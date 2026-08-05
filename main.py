from interface import Interface
from router import Route
from action import Launch
from voice import Voice
import threading
from interpreter import AtlasInterpreter

class Main:
    def __init__(self):
        self.interpreter=AtlasInterpreter()
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
    def voice_exit_handle(self,cmd):
        cmd=cmd.lower().strip()
        return cmd in (
            "exit",
            "sleep",
            "stop listening",
            "go back to sleep"
        )
    def run(self,mode="keyboard"):
        if mode=="keyboard":
            self.keyboard_input()
        elif mode=="voice":
            print("Voice command session started.")
            while True:
                try:
                    cmd=self.voice.voice_cmd()
                    if not cmd:
                        self.voice.error_return(
                            "didn't receive any command",
                            speak=False
                        )
                        self.voice.reset_command_audio()
                        print("Ready for next command.")
                        continue
                    if self.voice_exit_handle(cmd):
                        print("Voice command session ended.")
                        self.voice.reset_command_audio()
                        return
                    cmd=self.interpreter.interpret(cmd)
                    print(cmd)
                    response=self.home(cmd)
                    if not response:
                        self.voice.error_return(
                            "received invalid command",
                            speak=False
                        )
                    self.voice.reset_command_audio()
                    print("Ready for next command.")
                except Exception as e:
                    print(f"Voice command session error: {e}")
                    self.voice.error_return(
                        "received invalid command",
                        speak=False
                    )
                    self.voice.reset_command_audio()
                    print("Ready for next command.")
                    continue
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
            cmd=self.interpreter.interpret(cmd)
            print(cmd)
            self.home(cmd)
    def home(self,cmd):
        action,resource=self.route.evaluate(cmd)
        print(f"Executing action: {action}, resource: {resource}")
        if action=="open":
            result=self.launch.open(resource)
        elif action=="search":
            result=self.launch.search(resource)
        elif action=='create':
            workspace_resources=self.interface.workspace_query()
            self.route.create_guide(resource,workspace_resources)
            return True
        elif action=="load":
            if not resource:
                self.interface.error_handle("Workspace doesnot exist.")
                return False
            success=False
            for index,data_list in enumerate(resource):
                for data in data_list:
                    if index==0:
                        result=self.launch.open(data)
                        success=success or result.success
                    elif index==1:
                        result=self.launch.search(data)
                        success=success or result.success
                    elif index==2:
                        result=self.launch.open(data[0],url=data[1])
                        success=success or result.success
            return success
        elif action=="view":
            if not resource:
                self.interface.error_handle("Workspace doesnot exist.")
                return False
            self.interface.show_resources(resource)
            choice=self.interface.choice_query()
            if not choice:
                return False
            symbols=self.interface.delete_query()
            self.route.delete_divert(symbols)
            return True
        elif action=="system":
            self.launch.system_cmd(resource)
            return True
        else:
            self.interface.error_handle("Invalid command!")
            return False
        if not result.success:
            self.interface.error_handle(result.error)
        else:
            return True
    

Main().run()
