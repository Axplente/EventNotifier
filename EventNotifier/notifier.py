import os
import json
import time
from datetime import datetime, date

from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

from storage import get_data_path
from config import ICON_PATH


def notifier_main():
    file_path = get_data_path()

    # Small delay before startup
    time.sleep(30)

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    check_event_and_notify(data, file_path)


def check_event_and_notify(data, file_path):
    events = data.get("events", [])
    today = date.today()
    today_str = today.isoformat()
    changed = False

    for ev in events:
        if not ev.get("enabled", True):
            continue

        try:
            base_date = datetime.fromisoformat(ev["date"]).date()
        except Exception:
            continue

        repeat = ev.get("repeat", "none")

        # ---- Date resolution ----
        if repeat == "yearly":
            if base_date >= today:
                ev_date = base_date
            else:
                ev_month = base_date.month
                ev_day = base_date.day

                try:
                    this_year_date = date(today.year, ev_month, ev_day)
                except ValueError:
                    continue

                if this_year_date >= today:
                    ev_date = this_year_date
                else:
                    try:
                        ev_date = date(today.year + 1, ev_month, ev_day)
                    except ValueError:
                        continue
        else:
            ev_date = base_date
        # --------------------------

        delta = (ev_date - today).days
        if delta < 0:
            continue

        alert_days = ev.get("alert", 0)
        skip_list = ev.get("skip", [])
        last_notified = ev.get("last_notified")

        if 0 <= delta <= alert_days and delta not in skip_list and last_notified != today_str:
            ev["last_notified"] = today_str
            changed = True

            text = build_message(ev, delta)
            rt = ev.get("reminder_type", "popup").lower()

            if rt == "popup":
                show_popup(text)
            elif rt == "notification":
                show_notification(text)
            elif rt == "both":
                show_popup(text)
                show_notification(text)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


def build_message(ev, delta):
    name = ev.get("name", "")
    title = ev.get("event", "")
    date_str = ev.get("date", "")

    if delta > 0:
        line_days = f"{delta} day{'s' if delta != 1 else ''} until {title}"
    else:
        line_days = f"Today is {title}"

    return f"{name}\n{line_days}\n{date_str}"


def show_popup(text):
    app = QApplication.instance()
    created_app = False

    if app is None:
        app = QApplication([])
        created_app = True

    msg = QMessageBox()
    msg.setWindowTitle("Event Reminder")
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)
    msg.exec()

    if created_app:
        app.quit()


def show_notification(text):
    app = QApplication.instance()
    created_app = False

    if app is None:
        app = QApplication([])
        created_app = True

    tray = QSystemTrayIcon(QIcon(ICON_PATH), app)
    tray.setVisible(True)
    tray.showMessage("Event Reminder", text, QSystemTrayIcon.Information, 10000)

    if created_app:
        QTimer.singleShot(11000, app.quit)
        app.exec()