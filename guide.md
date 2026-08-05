# Atlas — Setup & Usage Guide

## 1. Overview

Atlas is a Windows desktop assistant that combines:

* Voice input
* Wake-word detection
* Speech-to-text transcription
* A fine-tuned language model for command interpretation
* Application discovery
* Application launching
* Web searching
* Workspace creation and loading
* SQLite-based local storage
* Keyboard and voice interaction

Atlas uses a modular architecture so the voice system, language-model interpreters, routing logic, discovery system, database, and execution layer remain separate.

---

## 2. Requirements

### Operating System

* Windows 10 or Windows 11

### Python

Atlas currently targets:

```text
Python 3.13
```

Using the same Python version across development and deployment is recommended.

### Hardware

For the current voice configuration:

* NVIDIA GPU recommended
* CUDA-compatible PyTorch installation
* Microphone
* Speakers/headphones

CPU execution is possible for some components, but the current voice configuration uses CUDA for Faster-Whisper.

---

## 3. Project Structure

A simplified project structure is:

```text
atlas/
│
├── main.py
├── voice.py
├── interpreter.py
├── atlasreg.py
├── discover.py
├── router.py
├── interface.py
├── action.py
├── url_generator.py
│
├── data/
│   ├── atlas-interpreter/
│   └── wakeup-interpreter/
│
└── Registry.db
```

### Main components

| File               | Responsibility                                          |
| ------------------ | ------------------------------------------------------- |
| `main.py`          | Application orchestration and interaction loops         |
| `voice.py`         | Audio capture, VAD, wake detection and transcription    |
| `interpreter.py`   | Atlas command language model                            |
| `discover.py`      | Application/path/workspace discovery                    |
| `atlasreg.py`      | SQLite persistence                                      |
| `router.py`        | Converts interpreted commands into executable resources |
| `interface.py`     | Keyboard-based interaction                              |
| `action.py`        | Executes applications, URLs and system actions          |
| `url_generator.py` | Generates search URLs                                   |

---

## 4. Environment Setup

Create a virtual environment:

```powershell
py -3.13 -m venv .venv313
```

Activate it:

```powershell
.venv313\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 5. PyTorch / CUDA

The current `voice.py` configuration uses:

```python
WhisperModel(
    "base",
    device="cuda",
    compute_type="float16"
)
```

Therefore, the machine must have a compatible NVIDIA CUDA environment for GPU inference.

Verify PyTorch:

```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

Expected result:

```text
True
```

If it prints:

```text
False
```

the voice pipeline may not run with the current configuration.

---

## 6. Microphone Configuration

The current implementation uses:

```python
self.input_device = 1
```

This is a machine-specific configuration.

If the microphone index changes, Atlas may listen to the wrong device or fail to initialize.

List available devices:

```powershell
python -c "import sounddevice as sd; print(sd.query_devices())"
```

Find the desired input device and update:

```python
self.input_device = 1
```

to the appropriate index.

### Recommended future improvement

Replace the hardcoded index with device-name or automatic device selection.

---

## 7. Running Atlas

From the project root:

```powershell
python main.py
```

Atlas starts its voice detection system and keyboard interface.

The terminal should show something similar to:

```text
Audio detection started.
Type Exit to close.
Enter the command:
```

---

## 8. Keyboard Mode

Keyboard commands are entered directly into the terminal.

Example:

```text
open chrome
```

The command is sent to the Atlas interpreter.

The interpreter produces a structured command such as:

```text
ACTION: open, TARGET: chrome
```

The router then resolves the target and the launcher executes it.

---

## 9. Voice Mode

The voice pipeline follows this sequence:

```text
Microphone
    ↓
Audio Stream
    ↓
Audio Queue
    ↓
Silero VAD
    ↓
Speech Segment
    ↓
Faster-Whisper
    ↓
Wakeup Interpreter
    ↓
Atlas Command Session
    ↓
Atlas Interpreter
    ↓
Router
    ↓
Action
```

### Wake detection

Atlas continuously listens for speech.

Silero VAD determines whether an audio frame contains speech.

When an utterance ends, Faster-Whisper transcribes it.

The transcription is passed to the wakeup interpreter.

Atlas only enters command mode when the wakeup interpreter produces a result that is parsed as:

```text
true
```

---

## 10. Voice Command Session

After a valid wake event, Atlas starts a command-listening session.

The user can issue commands without repeating the wake word for every command.

For example:

```text
Atlas
    ↓
open chrome
    ↓
search youtube python tutorial
    ↓
open vscode
    ↓
sleep
```

The session ends when the user says a supported sleep/exit phrase such as:

```text
sleep
stop listening
go back to sleep
```

---

## 11. Speech Detection

Silero VAD operates on fixed-size frames.

The current configuration uses:

```python
self.vad_frame_samples = 512
self.samplerate = 16000
```

Therefore:

```text
512 / 16000 = 0.032 seconds
```

Each VAD frame represents approximately:

```text
32 ms
```

The recording system accumulates these frames into an utterance.

Speech ends after the configured silence duration:

```python
self.silence_limit = 0.8
```

Wakeup detection uses:

```python
self.wakeup_silence_limit = 0.5
```

---

## 12. Pre-buffer

Atlas maintains a small audio buffer before speech is detected.

Current configuration:

```python
self.pre_buffer_duration = 0.3
```

This helps prevent the beginning of a word from being cut off when VAD detects speech slightly after the user actually starts speaking.

---

## 13. Speech-to-Text

Atlas uses Faster-Whisper:

```python
WhisperModel(
    "base",
    device="cuda",
    compute_type="float16"
)
```

The recorded NumPy audio is passed directly to the model.

The resulting segments are combined into one string and normalized before being passed to the next component.

---

## 14. Wakeup Model

The wakeup interpreter is a fine-tuned language model stored under:

```text
data/wakeup-interpreter/
```

Its purpose is intentionally narrow:

```text
speech transcription
        ↓
wakeup interpreter
        ↓
true / false
```

It should not execute Atlas commands.

Its only job is deciding whether the current utterance should activate Atlas.

---

## 15. Atlas Interpreter

The main interpreter is stored under:

```text
data/atlas-interpreter/
```

It converts natural-language commands into structured actions.

For example:

```text
Can you open Chrome?
```

may become:

```text
ACTION: open, TARGET: chrome
```

The router then handles the structured output.

---

## 16. Workspace System

Atlas can store groups of resources as workspaces.

A workspace may contain:

* Applications
* URLs
* URLs associated with a specific browser

Example concept:

```text
Python Workspace
├── VS Code
├── GitHub
├── Stack Overflow
└── Documentation
```

The workspace information is stored in:

```text
Registry.db
```

---

## 17. SQLite Database

Atlas uses SQLite for local persistence.

The database stores:

### Paths

```text
App → Path
```

### Workspaces

```text
Workspace
Type
Resources
Browser
```

The SQLite connection uses:

```python
check_same_thread=False
```

because the voice system and main application can operate in different threads.

A lock protects database operations from concurrent access.

---

## 18. Application Discovery

Atlas attempts to find applications through several mechanisms.

### 1. Atlas database

Previously discovered paths are checked first.

### 2. Windows App Paths registry

Atlas searches:

```text
HKEY_LOCAL_MACHINE
\SOFTWARE
\Microsoft
\Windows
\CurrentVersion
\App Paths
```

### 3. Start Menu shortcuts

Atlas searches `.lnk` files in Windows Start Menu directories.

### 4. System PATH

Atlas can also use:

```python
shutil.which()
```

to determine whether an executable is available through the system PATH.

---

## 19. Search

Atlas supports predefined search engines.

Examples include:

```text
google
youtube
github
stackoverflow
reddit
wikipedia
bing
amazon
pypi
npm
mdn
```

A search command is converted into a URL and opened through the default browser.

---

## 20. Troubleshooting

### Atlas wakes up from random noise

This is primarily a voice-pipeline/model-quality problem.

Possible causes:

* VAD threshold too low
* Background speech
* Environmental noise
* Poor microphone positioning
* Whisper hallucination
* Wakeup model false positives

The wakeup model should be evaluated using real background-noise samples before changing the rest of the architecture.

---

### Whisper produces incorrect transcriptions

Faster-Whisper is not guaranteed to produce perfect transcription.

Potential causes include:

* Background noise
* Low microphone signal
* Poor microphone placement
* Short audio segments
* Overlapping speech
* Wakeup audio containing unrelated speech

The current model is:

```text
base
```

Larger Whisper models can improve transcription quality at the cost of inference speed and GPU memory.

---

### SQLite thread error

If SQLite reports:

```text
SQLite objects created in a thread can only be used in that same thread
```

the connection was created in one thread and accessed from another.

Atlas addresses this using:

```python
check_same_thread=False
```

and a thread lock.

Database access should still be treated as a shared resource.

---

### VAD frame-size error

Silero VAD expects supported frame sizes.

At 16 kHz, the streaming model expects:

```text
512 samples
```

for each frame.

Therefore, passing 1600 samples directly into the streaming VAD model causes an error.

---

## 21. Model Files

The model adapters under:

```text
data/
```

are part of Atlas's inference system.

Do not remove them unless the interpreter code is changed to use different models.

If model files are too large for the Git repository, use Git LFS or distribute them separately rather than committing large binaries directly.

---

## 22. Development Workflow

Before committing changes:

```powershell
python -m py_compile main.py voice.py interpreter.py discover.py router.py interface.py action.py atlasreg.py url_generator.py
```

Then test:

1. Keyboard command parsing
2. Application discovery
3. Application launching
4. Database operations
5. Workspace creation/loading
6. Voice transcription
7. Wake detection
8. Voice command execution

Do not modify several independent components at once when debugging. Change one subsystem, test it, then continue.

---

## 23. Current Limitations

Atlas is currently a prototype rather than a production-grade desktop agent.

Known limitations include:

* Voice transcription quality depends heavily on microphone and environment.
* Wake detection can produce false positives in noisy environments.
* Input device selection is currently machine-specific.
* The voice pipeline depends on GPU availability for its current configuration.
* The natural-language interpreter can produce incorrect structured commands.
* The application discovery system is Windows-specific.
* Workspace storage is local to the machine.
* Some system actions are Windows-specific.

These limitations are useful engineering boundaries rather than reasons to hide the current implementation.

---

## 24. Development Principle

Atlas should evolve by improving one subsystem at a time:

```text
Input
  ↓
Understanding
  ↓
Routing
  ↓
Resource Discovery
  ↓
Execution
  ↓
Feedback
```

Each layer should have a clear responsibility and should be testable independently.

This separation makes future features easier to add without rewriting the entire application.
