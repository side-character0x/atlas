# Atlas

**Atlas** is a Windows desktop assistant built in Python that combines traditional system automation with locally running AI models.

The project started as a command-routing and application-launching system and evolved into a voice-controlled desktop assistant with custom-trained language-model adapters for wake-word interpretation and command interpretation.

## Features

* Voice-controlled desktop interaction
* Wake-word detection using a custom fine-tuned language-model adapter
* Speech detection using Silero VAD
* Speech-to-text using Faster-Whisper
* Local command interpretation using a fine-tuned Qwen adapter
* Application discovery through:

  * Windows Registry
  * Windows Start Menu shortcuts
  * System executable lookup
  * Stored application paths
* Application launching
* Web searching through configurable search engines
* Workspace creation and loading
* Workspace resource management
* SQLite-based application and workspace registry
* Keyboard and voice command interfaces
* Text-to-speech error responses
* CUDA acceleration when supported

## Architecture

Atlas is organized around a pipeline rather than putting all functionality into one file.

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │    Interface     │
                    │ Keyboard / Voice │
                    └────────┬─────────┘
                             │
                ┌────────────▼────────────┐
                │     Voice Pipeline      │
                │                         │
                │ Silero VAD              │
                │        ↓                │
                │ Faster-Whisper          │
                │        ↓                │
                │ Wakeup Interpreter     │
                └────────────┬────────────┘
                             │
                       Wake detected
                             │
                ┌────────────▼────────────┐
                │   Command Pipeline      │
                │                         │
                │ Faster-Whisper          │
                │        ↓                │
                │ Atlas Interpreter       │
                │        ↓                │
                │ Route / Parse command   │
                └────────────┬────────────┘
                             │
                    ┌────────▼─────────┐
                    │      Action      │
                    │                  │
                    │ Open application │
                    │ Search web       │
                    │ Load workspace   │
                    │ System command   │
                    └──────────────────┘
```

## Project Structure

```text
Atlas/
│
├── main.py
├── voice.py
├── interpreter.py
├── atlasreg.py
├── discover.py
├── router.py
├── action.py
├── interface.py
├── url_generator.py
│
├── data/
│   ├── atlas-interpreter/
│   └── wakeup-interpreter/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## AI Components

Atlas currently uses multiple models, each with a separate responsibility.

### Faster-Whisper

Faster-Whisper converts captured speech into text.

```text
Audio
  ↓
Faster-Whisper
  ↓
"open chrome"
```

The model is configured to use CUDA and FP16 when supported by the current installation.

### Silero VAD

Silero Voice Activity Detection determines whether an audio frame contains speech.

It allows Atlas to record dynamically rather than recording a fixed-length audio file for every interaction.

```text
Audio stream
     ↓
   VAD
     ↓
Speech detected
     ↓
Collect audio
     ↓
Silence detected
     ↓
Process utterance
```

### Wakeup Interpreter

Atlas uses a separate fine-tuned Qwen adapter to determine whether a spoken utterance should activate the assistant.

```text
Whisper transcription
        ↓
Wakeup Interpreter
        ↓
True / False
```

Separating wake interpretation from command interpretation prevents the main command model from being responsible for wake-word classification.

### Atlas Interpreter

The main Atlas interpreter uses a fine-tuned Qwen adapter to convert natural-language commands into a structured action representation.

For example:

```text
User:
open chrome

Atlas Interpreter:
ACTION: open, TARGET: chrome
```

The router then converts that representation into an executable operation.

## Application Discovery

Atlas does not rely on a single hardcoded path for applications.

When an application is requested, Atlas can attempt several discovery mechanisms:

```text
Stored registry
      ↓
Windows App Paths
      ↓
Start Menu shortcuts
      ↓
System executable lookup
      ↓
Requested target
```

This allows commands such as:

```text
open chrome
open vscode
```

without requiring the user to manually configure every executable path.

## Workspaces

Atlas can store groups of resources as workspaces.

A workspace can contain applications and URLs.

For example:

```text
Programming Workspace

VS Code
Chrome
GitHub
Stack Overflow
```

Loading the workspace allows Atlas to restore the associated resources.

Workspace information is stored in SQLite.

## Database

Atlas uses SQLite to store:

* application paths
* workspace names
* workspace resources
* resource types
* associated browsers

The database is created automatically when Atlas starts.

The database file is local application state and should not be committed to the repository.

## Voice Interaction

The intended interaction flow is:

```text
Atlas listening
      ↓
Speech detected
      ↓
Wakeup model
      ↓
Wake detected?
   ↙        ↘
 No          Yes
 ↓            ↓
Continue    Listen for command
              ↓
           Whisper
              ↓
        Atlas Interpreter
              ↓
            Router
              ↓
            Action
              ↓
        Return to wake detection
```

A wake event starts a command session. After the command is processed, Atlas returns to wake detection.

## Example Commands

Examples of supported command patterns include:

```text
open chrome
open vscode
search google python decorators
search youtube machine learning
```

Workspace operations can also be represented through the command interpreter.

## Requirements

Atlas is currently designed primarily for Windows.

The project requires Python and several machine-learning and audio dependencies.

The exact dependency versions should be installed from:

```text
requirements.txt
```

A CUDA-capable NVIDIA GPU is recommended for the current voice configuration.

CPU execution may be possible with appropriate model configuration, but inference performance will differ.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Atlas
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The trained adapter models must also be available under:

```text
data/
├── atlas-interpreter/
└── wakeup-interpreter/
```

## Running Atlas

Run:

```bash
python main.py
```

Atlas starts its background voice-detection system and also provides keyboard interaction.

## Configuration

Some settings are currently defined directly in `voice.py`, including:

* microphone device
* sample rate
* VAD frame size
* silence thresholds
* maximum utterance duration
* Whisper model configuration

The current implementation is intentionally simple, but these values can later be moved into a configuration file.

## Current Limitations

Atlas is a personal project and is not yet intended to be a production-grade desktop agent.

Known limitations include:

* Windows-specific application discovery
* microphone configuration currently depends on the local audio device configuration
* speech recognition quality depends heavily on microphone quality and background noise
* wake-word detection can produce false positives in noisy environments
* natural-language interpretation is limited by the training data of the custom adapters
* some application discovery mechanisms depend on Windows-specific paths and registry configuration
* CUDA configuration is hardware-dependent
* the project currently assumes a local model environment rather than providing a packaged one-click installation

These are known engineering limitations rather than hidden behavior.

## Design Goals

Atlas is being developed around several principles:

1. **Local execution**

   AI inference should run locally where practical.

2. **Separation of concerns**

   Voice processing, interpretation, routing, discovery, persistence, and execution should remain separate components.

3. **Model specialization**

   Different models should have specific responsibilities instead of using one model for every task.

4. **Deterministic execution**

   The language model should interpret the user's intent, while deterministic Python components perform the actual system operations.

5. **Extensibility**

   New actions should be addable without rewriting the entire application.

## Why Atlas?

Atlas is an experiment in building a complete AI-assisted desktop system rather than only calling an AI API.

The interesting part of the project is the interaction between:

```text
Machine Learning
       +
Speech Processing
       +
Natural Language Interpretation
       +
Software Architecture
       +
Operating System Automation
       +
Persistent State
```

The project is therefore also being used as a practical exercise in designing and debugging a multi-component software system.

## Development Status

**Status: Experimental / Personal Project**

Core functionality currently includes:

* application discovery
* application launching
* web searching
* workspace persistence
* voice activity detection
* speech recognition
* custom wake interpretation
* custom command interpretation
* keyboard and voice interaction

The voice pipeline is functional but still being improved for robustness against background noise and speech-recognition errors.

## Future Development

Potential future improvements include:

* better wake-word robustness
* improved speech recognition under noisy conditions
* configurable microphone selection
* centralized configuration
* structured logging
* automated tests
* improved command validation
* safer action execution
* more desktop actions
* better workspace management
* installer/distribution support
* improved model evaluation and training datasets

## Project Philosophy

Atlas is not intended to demonstrate that an AI model can perform every desktop task.

Instead, the architecture uses AI where probabilistic interpretation is useful and conventional software where deterministic behavior is preferable.

```text
AI
↓
Understand intent

Software
↓
Validate intent

Router
↓
Select operation

Action layer
↓
Execute operation
```

That separation is central to the project's design.
