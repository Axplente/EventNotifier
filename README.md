# Event Notifier

A lightweight desktop tool built with Python and PySide6 that helps you remember birthdays, anniversaries, and other important events — so you never miss a date again.

---

## Overview

Event Notifier is a simple desktop reminder application designed to run quietly in the background and notify you about important dates.

It was built as a personal learning project while exploring GUI development and Windows desktop packaging with Python.

---

## Features

* Modern GUI built with PySide6
* System tray + popup notifications
* Local JSON-based storage
* Background mode (`--notify`)
* Custom reminder offsets (days before events)
* Yearly recurring events
* Lightweight and fast

---

## Tech Stack

* Python 3.x
* PySide6 (Qt for Python)
* Standard libraries (os, json, datetime, uuid, time, winreg)
* Windows platform

---

## Installation & Usage

### 1. Clone the repository

```bash id="clone1"
git clone https://github.com/Axplente/EventNotifier.git
cd EventNotifier
```

### 2. Install dependencies

```bash id="install1"
pip install -r requirements.txt
```

### 3. Run the app

```bash id="run1"
python main.py
```

### Background mode

```bash id="bg1"
python main.py --notify
```

---

## Downloads

👉 Latest Release:
https://github.com/Axplente/EventNotifier/releases/latest

---

## Prebuilt Executable

A ready-to-use Windows executable is available in the Releases section.

### ⚠️ Windows SmartScreen Warning

Because the executable is not digitally signed, Windows may show:

> Windows protected your PC

This is normal for unsigned open-source applications and does not indicate malware.

You can safely run the program or inspect the source code.

---

## Building from Source

```bash id="build1"
pip install -r requirements.txt
pip install pyinstaller
```

```bash id="build2"
pyinstaller --onefile --windowed --icon=assets/Calendar.ico --add-data "assets;assets" --name EventNotifier main.py
```

Output:

```text id="output1"
dist/EventNotifier.exe
```

---

## What I Learned

* Building GUI apps with PySide6
* Windows notifications and system tray integration
* Persistent JSON data handling
* Structuring Python projects
* Packaging apps with PyInstaller

---

## License

MIT License

---

## About Me

Axplente — Developer from Bavaria, Germany
GitHub: https://github.com/Axplente
