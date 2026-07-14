import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import pyttsx3 as pt
from silero_vad import load_silero_vad, get_speech_timestamps

class Voice:
    def __init__(self,callback):
        self.engine=pt.init()
        self.whispermodel=WhisperModel("base",device="cpu",compute_type="int8")
        self.callback=callback
        self.sileromodel=load_silero_vad()
    def voice_cmd(self):
        try:
            print("Listening....")
            audio=sd.rec(samplerate=16000,frames=4*16000,channels=1,dtype="float32")
            sd.wait()
            print("loading..")
            sf.write("voice.wav",audio,16000)
            segments, info = self.whispermodel.transcribe("voice.wav")
            cmd = " ".join(segment.text for segment in segments)
            if "." in cmd:
                cmd=cmd.replace(".","")
            return cmd.lower()
        except UnboundLocalError:
            cmd=False
            return False
    def error_return(self,error):
        self.engine.say(error)
        self.engine.runAndWait()
    def audio_detection(self):
        while True:
            audio=sd.rec(samplerate=16000,frames=2*16000,channels=1,dtype="float32")
            sd.wait()
            speech=get_speech_timestamps(audio[:,0],self.sileromodel,sampling_rate=16000)
            if speech:
                sf.write("sample.wav",audio,16000)
                response=self.wakeup_detection()
                if response:
                    self.callback(mode="voice")
    def wakeup_detection(self):
        segments, info =self.whispermodel.transcribe("sample.wav")
        speech=" ".join(segment.text for segment in segments)
        if "computer" in speech.lower():
            return True
        else:
            return False