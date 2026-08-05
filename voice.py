import queue
import re
import threading
from collections import deque

import numpy as np
import sounddevice as sd
import pyttsx3 as pt
import torch

from faster_whisper import WhisperModel
from silero_vad import load_silero_vad

from interpreter import WakeupInterpreter


class Voice:

    def __init__(self, callback):

        self.engine = pt.init()

        self.whispermodel = WhisperModel(
            "base",
            device="cuda",
            compute_type="float16"
        )

        self.callback = callback
        self.wakeup_interpreter = WakeupInterpreter()
        self.vad = load_silero_vad()

        self.samplerate = 16000
        self.channels = 1
        self.dtype = "float32"

        self.vad_frame_samples = 512
        self.chunk_duration = (
            self.vad_frame_samples / self.samplerate
        )

        self.silence_limit = 0.8
        self.max_duration = 10.0

        self.wakeup_silence_limit = 0.5
        self.wakeup_max_duration = 3.0

        self.pre_buffer_duration = 0.3
        self.pre_buffer_chunks = max(
            1,
            int(
                self.pre_buffer_duration
                / self.chunk_duration
            )
        )
    
        self.audio_queue = queue.Queue()

        self.stream = None
        self.stream_lock = threading.Lock()

        self.running = False

    def _audio_callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        if status:
            print(f"Audio stream status: {status}")

        self.audio_queue.put(
            indata.copy()
        )

    def _start_stream(self):

        with self.stream_lock:

            if self.stream is not None:
                return

            self.stream = sd.InputStream(
                samplerate=self.samplerate,
                blocksize=self.vad_frame_samples,
                channels=self.channels,
                dtype=self.dtype,
                callback=self._audio_callback
            )

            self.stream.start()

    def _stop_stream(self):

        with self.stream_lock:

            if self.stream is not None:

                self.stream.stop()
                self.stream.close()
                self.stream = None

    def _clear_audio_queue(self):

        while True:

            try:
                self.audio_queue.get_nowait()

            except queue.Empty:
                break

    def _vad_probability(self, audio):

        audio_tensor = torch.from_numpy(
            audio[:, 0]
        )

        with torch.no_grad():

            probability = self.vad(
                audio_tensor,
                self.samplerate
            ).item()

        return probability

    def _normalize_text(self, text):

        text = text.lower()

        text = re.sub(
            r"[^\w\s]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _transcribe(self, audio_data):

        segments, info = self.whispermodel.transcribe(
            audio_data[:, 0],
            language="en"
        )

        text = " ".join(
            segment.text
            for segment in segments
        )

        return self._normalize_text(text)

    def _get_audio_chunk(self, timeout=0.1):

        try:

            return self.audio_queue.get(
                timeout=timeout
            )

        except queue.Empty:

            return None

    def _record_utterance(
        self,
        silence_limit,
        max_duration
    ):

        recording = []

        pre_buffer = deque(
            maxlen=self.pre_buffer_chunks
        )

        speech_started = False
        silence_time = 0.0
        utterance_time = 0.0

        while self.running:

            audio = self._get_audio_chunk()

            if audio is None:
                continue

            pre_buffer.append(audio)

            try:

                probability = self._vad_probability(
                    audio
                )

            except Exception as e:

                print(f"VAD error: {e}")
                continue

            has_speech = probability >= 0.5

            if has_speech:

                if not speech_started:

                    speech_started = True

                    recording.extend(
                        list(pre_buffer)
                    )

                    utterance_time = (
                        len(recording)
                        * self.chunk_duration
                    )

                    print("Speech detected.")

                else:

                    recording.append(audio)

                    utterance_time += (
                        self.chunk_duration
                    )

                silence_time = 0.0

            elif speech_started:

                recording.append(audio)

                silence_time += (
                    self.chunk_duration
                )

                utterance_time += (
                    self.chunk_duration
                )

                if silence_time >= silence_limit:

                    print("Speech ended.")
                    break

            if (
                speech_started
                and utterance_time >= max_duration
            ):

                print(
                    "Maximum utterance length reached."
                )
                break

        if not self.running:
            return None

        if not speech_started:
            return None

        return np.concatenate(
            recording,
            axis=0
        )

    def voice_cmd(self):

        try:

            print("Waiting for command...")

            self._clear_audio_queue()

            audio = self._record_utterance(
                silence_limit=self.silence_limit,
                max_duration=self.max_duration
            )

            if audio is None:

                print("No command detected.")
                return None

            print("Transcribing command...")

            command = self._transcribe(
                audio
            )

            print(
                f"You said: {command}"
            )

            return command

        except Exception as e:

            print(
                f"Voice command error: {e}"
            )

            return None

    def wakeup_detection(self, audio_data):

        try:
            speech = self._transcribe(audio_data)

            print(f"Wakeup transcription: {speech}")

            if not speech:
                print("Wakeup model result: ")
                print("Wakeup detected: False")
                return False

            result = self.wakeup_interpreter.interpret(speech)

            print(f"Wakeup model result: {result}")

            detected = self._parse_wakeup_result(result)

            print(f"Wakeup detected: {detected}")

            return detected

        except Exception as e:
            print(f"Wakeup detection error: {e}")
            return False

    def _parse_wakeup_result(self, result):

        if isinstance(result, bool):
            return result

        if result is None:
            return False

        result = self._normalize_text(str(result))

        return result == "true"

    def audio_detection(self):

        print(
            "Audio detection started."
        )

        self.running = True

        try:

            self._start_stream()

            while self.running:

                audio = self._record_utterance(
                    silence_limit=self.wakeup_silence_limit,
                    max_duration=self.wakeup_max_duration
                )

                self._clear_audio_queue()

                try:
                    self.vad.reset_states()
                except Exception:
                    pass

                if audio is None:
                    continue

                detected = self.wakeup_detection(
                    audio
                )

                self._clear_audio_queue()

                if detected:

                    print(
                        "Wake word detected."
                    )

                    self.callback(
                        mode="voice"
                    )

                    self._clear_audio_queue()

        except Exception as e:

            print(
                f"Audio detection error: {e}"
            )

        finally:

            self.running = False
            self._stop_stream()

            try:
                self.vad.reset_states()
            except Exception:
                pass

    def stop(self):

        self.running = False

        self._stop_stream()

        self._clear_audio_queue()

    def reset_command_audio(self):

        self._clear_audio_queue()

        try:
            self.vad.reset_states()
        except Exception:
            pass

    def error_return(self, error, speak=True):

        print(error)

        if not speak:
            return

        try:
            self.engine.say(error)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Voice error response failed: {e}")

