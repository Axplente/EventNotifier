# Event Notifier

A lightweight desktop tool built with Python and PySide6 that helps you remember birthdays, anniversaries, and other important events — so you never miss a date again.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Installation & Usage](#installation--usage)
* [Requirements](#requirements)
* [Downloads](#downloads)
* [Prebuilt Executable](#prebuilt-executable)
* [Building from Source](#building-from-source)
* [Screenshots](#screenshots)
* [What I Learned](#what-i-learned)
* [Maintenance](#maintenance)
* [License](#license)
* [About Me](#about-me)

---

## Overview

Event Notifier was created to solve a simple but personal problem: forgetting important dates. Since I spend most of my time on my computer, I built this tool to manage reminders directly on my desktop.

This project was my first public release and a learning experience in building and packaging a full Python GUI application.

---

## Features

* Modern GUI built with PySide6
* System tray + popup notifications
* Local persistent storage (JSON)
* Automatic startup mode (`--notify`)
* Custom reminder offsets (days before events)
* Yearly recurring events
* Flexible skip-day logic

---

## Tech Stack

* Python 3.x
* PySide6 (Qt for Python)
* Standard libraries: os, json, datetime, uuid, time, winreg
* Windows platform

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/Axplente/EventNotifier.git
cd EventNotifier
```

### 2. Set up environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the app

```bash
python main.py
```

### Background mode

```bash
python main.py --notify
```

---

## Requirements

All dependencies are listed in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## Downloads

👉 Latest Release:
https://github.com/Axplente/EventNotifier/releases/latest

---

## Prebuilt Executable

A prebuilt Windows executable is available in the Releases section.

### ⚠️ Windows SmartScreen Warning

Because the executable is not digitally signed, Windows may show:

> Windows protected your PC

This is normal for unsigned open-source software and does not indicate malware.

The full source code is available in this repository for review.

---

## Building from Source

### Install dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Build executable

```bash
pyinstaller --onefile --windowed --icon=assets/Calendar.ico --add-data "assets;assets" --name EventNotifier main.py
```

The executable will be created in:

```text
dist/EventNotifier.exe
```

---

## Screenshots

(Add screenshots here)

---

## What I Learned

* Building GUI applications with PySide6
* Event-driven programming
* Local data storage with JSON
* Windows system integration
* Packaging Python apps with PyInstaller

---

## Maintenance

Open to issues and feature requests.

---

## License

MIT License

---

## About Me

**Axplente** — Developer from Bavaria, Germany

GitHub: https://github.com/Axplente
