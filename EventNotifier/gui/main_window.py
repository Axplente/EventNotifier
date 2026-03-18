from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

from storage import get_data_path, load_data, save_data
from startup import update_windows_startup
from config import ICON_PATH
from utils import parse_skip_days
from gui.view_window import ViewWindow


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Notifier")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(800, 600)

        # ---------------- File Path & Data ----------------
        self.file_path = get_data_path()
        self.data = load_data(self.file_path)

        if "settings" not in self.data:
            self.data["settings"] = {"run_on_startup": False}

        self.layout = QVBoxLayout(self)

        # ---------------- Name Input ----------------
        self.layout.addWidget(QLabel("Person / Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Who is this event for?")
        self.name_input.setMinimumWidth(200)
        self.layout.addWidget(self.name_input)

        # ---------------- Event Input ----------------
        self.layout.addWidget(QLabel("Event Description:"))
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("Describe the event, e.g., Birthday")
        self.event_input.setMinimumWidth(200)
        self.layout.addWidget(self.event_input)

        # ---------------- Calendar ----------------
        self.layout.addWidget(QLabel("Event Date:"))
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumSize(400, 300)
        self.calendar.setMaximumSize(700, 450)
        self.calendar.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
        calendar_layout = QHBoxLayout()
        calendar_layout.addStretch()
        calendar_layout.addWidget(self.calendar)
        calendar_layout.addStretch()
        self.layout.addLayout(calendar_layout)

        # ---------------- Feedback ----------------
        self.feedback_label = QLabel("")
        self.layout.addWidget(self.feedback_label)

        # ---------------- View Events Button ----------------
        self.button_view = QPushButton("View Saved Events")
        self.layout.addWidget(self.button_view)
        self.button_view.clicked.connect(self.open_view_window)

        # ---------------- Done / Cancel Buttons ----------------
        self.button_done = QPushButton("Save Event")
        self.button_cancel = QPushButton("Cancel")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_done)
        button_layout.addWidget(self.button_cancel)

        # ---------------- Event Options Row ----------------
        self.event_types = QHBoxLayout()
        self.repeat_checkbox = QCheckBox("Repeat Yearly")
        self.reminder_type = QComboBox()
        self.reminder_type.addItems(["Popup", "Notification", "Both"])
        self.run_startup_checkbox = QCheckBox("Run on Startup?")
        self.event_types.addWidget(self.run_startup_checkbox)
        self.event_types.addWidget(self.repeat_checkbox)
        self.event_types.addWidget(self.reminder_type)
        self.layout.addLayout(self.event_types)

        # ---------------- Alert & Skip Row ----------------
        self.extra_options = QHBoxLayout()
        self.alert_label = QLabel("Alert days before:")
        self.alert_days_spin = QSpinBox()
        self.alert_days_spin.setMinimum(0)
        self.alert_days_spin.setMaximum(365)
        self.skip_label = QLabel("Skip days (optional):")
        self.skip_days = QLineEdit()
        self.extra_options.addWidget(self.alert_label)
        self.extra_options.addWidget(self.alert_days_spin)
        self.extra_options.addWidget(self.skip_label)
        self.extra_options.addWidget(self.skip_days)
        self.layout.addLayout(self.extra_options)

        # ---------------- Add Button Layout ----------------
        self.layout.addLayout(button_layout)

        # ---------------- Connections ----------------
        self.button_done.clicked.connect(self.save_event)
        self.button_cancel.clicked.connect(self.close)

        self.run_startup_checkbox.setChecked(
            self.data["settings"].get("run_on_startup", False)
        )
        self.run_startup_checkbox.stateChanged.connect(
            self.on_run_startup_change
        )


    # ---------------- Save Event ----------------
    def save_event(self):
        name = self.name_input.text().strip()
        event = self.event_input.text().strip()
        date_str = self.calendar.selectedDate().toPython().isoformat()
        repeat_value = "yearly" if self.repeat_checkbox.isChecked() else "none"
        reminder_type = self.reminder_type.currentText().lower()
        alert_days = self.alert_days_spin.value()
        skip_list = parse_skip_days(self.skip_days.text(), alert_days)

        if skip_list and max(skip_list) > alert_days:
            self.feedback_label.setText("Cannot skip a day beyond alert days")
            return

        if not name or not event:
            self.feedback_label.setText("Please fill in both Name and Event!")
            return

        new_event = {
            "name": name,
            "event": event,
            "date": date_str,
            "enabled": True,
            "repeat": repeat_value,
            "reminder_type": reminder_type,
            "alert": alert_days,
            "skip": skip_list
        }

        self.data.setdefault("events", []).append(new_event)
        save_data(self.file_path, self.data)

        # Clear inputs
        self.name_input.clear()
        self.event_input.clear()
        self.repeat_checkbox.setChecked(False)
        self.reminder_type.setCurrentIndex(0)
        self.alert_days_spin.setValue(0)
        self.skip_days.clear()
        self.feedback_label.setText(f"Saved: {name} - {event} - {date_str}")

    # ---------------- Open View Window ----------------
    def open_view_window(self):
        self.view_window = ViewWindow(self.data, self.file_path)
        self.view_window.show()

    # ---------------- Run on Startup ----------------
    def on_run_startup_change(self):
        checked = self.run_startup_checkbox.isChecked()
        self.data["settings"]["run_on_startup"] = checked
        save_data(self.file_path, self.data)
        update_windows_startup(checked)

    def closeEvent(self, event):
        if hasattr(self, "view_window") and self.view_window is not None and self.view_window.isVisible():
            self.view_window.close()
        super().closeEvent(event)