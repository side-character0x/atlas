# Atlas

Atlas is a command-line productivity assistant designed to automate the initialization of development resources. It reduces the repetitive process of opening applications, websites, files, and workspaces by allowing users to launch them through simple keyboard or voice commands.

> **Status:** Prototype (Version 0.1)

---

## Features

### Resource Initialization
Launch commonly used resources with a single command.

Supported resource types:
- Windows applications (.exe)
- Local files and folders
- URLs and websites

---

### Voice Commands
Atlas includes an experimental voice interface.

Current voice pipeline:
- Voice Activity Detection (Silero VAD)
- Speech-to-Text (Faster-Whisper)
- Wake-word detection
- Command execution

Example:

```text
Computer
Open Chrome
```

---

### Workspace Management

Create a workspace containing multiple resources and launch them simultaneously.

Example:

```text
create workspace python
```

Save resources such as:

- VS Code
- Chrome
- Documentation
- GitHub Repository
- Terminal

Later,

```text
load workspace python
```

will initialize the complete development environment instantly.

---

## Current Architecture

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

Voice commands run on a background thread while keyboard commands remain available.

---

## Technologies Used

- Python
- Faster-Whisper
- Silero VAD
- SoundDevice
- SoundFile
- pyttsx3
- SQLite

---

## Current Limitations

This repository represents an early prototype.

Known limitations include:

- Wake-word detection is still experimental.
- Speech recognition accuracy varies depending on microphone quality and pronunciation.
- Command validation requires improvement.
- Voice command processing is not yet optimized for production use.
- Error handling and edge-case coverage are still under development.

---

## Future Improvements

Planned enhancements include:

- Improved speech recognition accuracy
- Better wake-word detection
- Fuzzy command matching
- Plugin architecture
- Background service mode
- Smarter command parsing
- Performance optimization
- Improved validation and error recovery

---

## Motivation

Atlas was built to eliminate repetitive setup tasks during development. Instead of manually opening the same applications, folders, browser tabs, and project resources every day, Atlas automates the process through reusable workspaces and voice commands.

The long-term goal is to evolve Atlas into a modular productivity assistant for developers.

---

## Project Status

This project is currently under active development and serves as a learning project focused on software architecture, automation, threading, voice interfaces, and command routing.