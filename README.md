# Event Notifier

A lightweight desktop tool built with Python and PySide6 that helps you remember birthdays, anniversaries, and other important events — so you never miss a date again.

---

## Overview

Event Notifier was created to solve a simple but personal problem: I kept forgetting birthdays. Since I spend most of my time on my computer, I decided to teach myself GUI development with PySide6 and build a reminder tool from scratch.

This project was my first public release — and my crash course in packaging, organizing, and learning a new framework within four days of focused coding.

---

## Features

- Modern GUI built with PySide6  
- Popup and system tray notifications (or both)  
- Persistent data stored locally in JSON format  
- Automatic startup using Windows Registry (--notify mode)  
- Custom alerts: choose how many days before an event  
- Yearly repeats for birthdays and recurring events  
- Skip specific alert days for custom reminder logic  

---

## Tech Stack

- **Language:** Python 3.x  
- **GUI Framework:** PySide6 (Qt for Python)  
- **Libraries:** os, json, datetime, uuid, time, winreg  
- **Platform:** Windows  

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
venv\Scripts\activate  # Windows
pip install PySide6
```

### 3. Run the app
```bash
python main.py
```

**Startup mode:** `python main.py --notify` (runs silently, checks events, notifies if needed)

---

## Screenshots

![Main Window](https://github.com/user-attachments/assets/e9c14ace-51c8-4f19-b346-a650ccc870ed)

![View Window](https://github.com/user-attachments/assets/47f7da1a-8cf1-41ff-87e7-0429fd9910c5) 

![Edit Window](https://github.com/user-attachments/assets/7f6b91a4-bb63-4b21-9750-6c2f5d531989)

---

## What I Learned

- Building a complete GUI application in Python  
- PySide6 widgets, signals, layouts, and event handling  
- Windows system tray notifications and registry integration  
- Persistent JSON data management and settings  
- Structuring a Python project for readability  

---

## Maintenance

Open to bug reports and feature requests! If people find it useful and ask for improvements, I'll consider adding them.

---

## License

[MIT License](LICENSE)

---

## About Me

**Axplente** — Aspiring developer from Bavaria, Germany.  
Turning everyday problems into practical software solutions.

**GitHub:** [@Axplente](https://github.com/Axplente)

---

⭐ Star this repo if you find it useful!
