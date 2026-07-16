# Atlas User Guide

> Complete usage guide for Atlas v0.1

Atlas is a command-line productivity assistant that automates repetitive setup tasks by launching applications, websites, and complete development workspaces through keyboard or voice commands.

---

# Table of Contents

- [General Commands](#general-commands)
- [Open Applications](#open-applications)
- [Search the Web](#search-the-web)
- [Workspaces](#workspaces)
- [View Workspaces](#view-workspaces)
- [System Commands](#system-commands)
- [Voice Mode](#voice-mode)
- [Application Discovery](#application-discovery)
- [Current Limitations](#current-limitations)
- [Tips](#tips)
- [Example Session](#example-session)

---

# General Commands

| Command | Description |
|---------|-------------|
| `open <application>` | Launch an application |
| `search <engine> <query>` | Search using a supported search engine |
| `create workspace <name>` | Create a new workspace |
| `load workspace <name>` | Launch all resources inside a workspace |
| `view workspace <name>` | View and manage a workspace |
| `system <action>` | Execute Windows power commands |
| `exit` | Close Atlas |

---

# Open Applications

Launch Windows applications by name.

## Syntax

```text
open <application>
```

## Examples

```text
open chrome

open vscode

open notepad

open microsoft edge
```

Atlas attempts to locate applications in the following order:

1. Atlas Registry
2. Windows Registry
3. Windows Start Menu
4. Windows PATH

Successful lookups are automatically cached for future launches.

---

# Search the Web

Search directly from the terminal.

## Syntax

```text
search <engine> <query>
```

## Examples

```text
search google python decorators

search youtube pandas tutorial

search github requests

search stackoverflow sqlite error
```

## Supported Search Engines

- Google
- YouTube
- GitHub
- Stack Overflow
- Reddit
- Wikipedia
- DuckDuckGo
- Bing
- Amazon
- eBay
- PyPI
- npm
- MDN
- GeeksForGeeks
- W3Schools
- Medium
- Quora
- IMDb

---

# Workspaces

Workspaces allow multiple resources to be launched simultaneously.

## Create a Workspace

```text
create workspace python
```

Atlas will request the following information for each resource.

| Input | Description |
|--------|-------------|
| Resource | Application name or URL |
| Type | `app` or `url` |
| Browser | Optional browser for URLs |

When finished, type:

```text
end
```

### Example

```text
Resource : chrome
Type     : app

Resource : vscode
Type     : app

Resource : https://github.com
Type     : url

Browser  : chrome

Resource : end
```

---

# Load a Workspace

```text
load workspace python
```

Atlas launches every application and website stored inside the workspace.

---

# View Workspaces

```text
view workspace python
```

Displays every resource stored in the workspace.

You may optionally delete one or more resources.

Accepted formats:

```text
1,2,4
```

or

```text
1 2 4
```

---

# System Commands

Available commands:

```text
system shutdown

system restart

system sleep
```

These execute the corresponding Windows power operation.

---

# Voice Mode

## Wake Word

```text
Computer
```

## Example

```text
Computer

Open Chrome
```

## Voice Pipeline

```text
Voice Activity Detection
        ↓
Wake-word Detection
        ↓
Speech-to-Text
        ↓
Command Execution
```

Voice mode runs independently while keyboard commands remain available.

---

# Application Discovery

Atlas searches for applications using the following priority.

```text
Atlas Registry
        ↓
Windows Registry
        ↓
Windows Start Menu
        ↓
Windows PATH
```

Every successful lookup is cached to improve future launch speed.

---

# Current Limitations

- Windows only
- Wake-word detection is experimental
- Voice recognition accuracy depends on microphone quality
- Error handling is still being expanded
- Voice processing is not yet optimized for production use

---

# Tips

- Store frequently used development environments as workspaces.
- Browser selection is optional for URLs.
- Atlas remembers previously discovered applications.
- Use application names instead of executable paths whenever possible.

---

# Example Session

```text
> create workspace python

Resource : chrome
Type     : app

Resource : vscode
Type     : app

Resource : https://github.com
Type     : url

Browser  : chrome

Resource : end

Workspace created successfully.
```

Later...

```text
> load workspace python

Launching...

✓ Chrome

✓ VS Code

✓ GitHub

Workspace loaded successfully.
```

---

# Need Help?

If you encounter an issue or have suggestions for Atlas, please open an issue on the GitHub repository.