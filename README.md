# Atlas

A Python productivity assistant that eliminates repetitive setup tasks by launching applications, websites, files, and complete development workspaces through simple keyboard or voice commands.

Instead of manually opening the same tools every day, Atlas lets you start your working environment with a single command.

> Status: Active Prototype (v0.1)

---

# Why Atlas?

Developers often begin each session by opening the same applications, folders, browser tabs, and documentation.

Atlas automates that process.

Instead of

- Opening Chrome
- Opening VS Code
- Opening GitHub
- Opening documentation
- Opening Terminal

you can simply run

```text
load workspace python
```

and Atlas launches everything automatically.

---

# Features

### Launch Applications

```text
open chrome

open vscode

open notepad
```

Atlas automatically discovers applications using:

- Atlas Registry
- Windows Registry
- Start Menu
- Windows PATH

Discovered applications are cached for faster future launches.

---

### Search the Web

Search directly from the terminal.

```text
search google python decorators

search github requests library

search youtube pandas tutorial
```

Supported engines include Google, GitHub, Stack Overflow, YouTube, Reddit, MDN and more.

---

### Workspaces

Save frequently used resources into reusable workspaces.

Example:

```text
create workspace python
```

Store

- VS Code
- Chrome
- GitHub
- Documentation
- Terminal

Later

```text
load workspace python
```

launches the complete environment instantly.

---

### Voice Commands

Atlas includes an experimental voice interface.

Example

```text
Computer

Open Chrome
```

Voice Pipeline

```
Voice Activity Detection
        ↓
Wake Word Detection
        ↓
Speech Recognition
        ↓
Command Execution
```

Keyboard commands remain available while voice mode runs in the background.

---

# Architecture

```
User
   │
   ▼
Interface
   │
   ▼
Router
   │
   ▼
Main Controller
   │
   ▼
Action Executor
```

Each layer has a dedicated responsibility, making Atlas easier to extend and maintain.

---

# Technologies

- Python
- SQLite
- Faster Whisper
- Silero VAD
- Requests
- SoundDevice
- pyttsx3

---

# Example Session

```text
> load workspace python

Launching...

✓ VS Code

✓ Chrome

✓ GitHub

✓ Python Documentation

Workspace loaded successfully.
```

---

# Current Status

Atlas is an actively developed prototype.

Current development focuses on

- Improving command validation
- Better wake-word detection
- Smarter routing
- Improved voice recognition
- Better error handling
- Performance optimization

---

# Project Goal

Atlas is not intended to be another chatbot.

The long-term objective is to build a modular productivity assistant focused on automation and workflow management for developers.
