from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from storage import save_data
from config import ICON_PATH
from utils import parse_skip_days


class EditWindow(QtWidgets.QWidget):
    event_saved = Signal()

    def __init__(self, data, file_path, selected_event):
        super().__init__()
        
        self.setWindowTitle("Edit Event")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(600, 400)

        # -------- Configs --------
        self.data = data
        self.file_path = file_path
        self.event_data = selected_event
        self.layout = QVBoxLayout(self)

        # -------- Name Input --------
        self.layout.addWidget(QLabel("Person / Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Who is this event for?")
        self.name_input.setMinimumWidth(200)
        self.layout.addWidget(self.name_input)

        # -------- Event Description --------
        self.layout.addWidget(QLabel("Event Description:"))
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("Describe the event, e.g., Birthday")
        self.event_input.setMinimumWidth(200)
        self.layout.addWidget(self.event_input)

        # -------- Calendar for Date --------
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

        # -------- Feedback --------
        self.feedback_label = QLabel("")
        self.layout.addWidget(self.feedback_label)

        # -------- Done / Cancel Buttons --------
        self.button_done = QPushButton("Save Changes")
        self.button_cancel = QPushButton("Cancel")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_done)
        button_layout.addWidget(self.button_cancel)
        self.layout.addLayout(button_layout)

        # -------- Event Options Row --------
        self.event_types = QHBoxLayout()
        self.repeat_checkbox = QCheckBox("Repeat Yearly")
        self.reminder_type = QComboBox()
        self.reminder_type.addItems(["Popup", "Notification", "Both"])
        self.event_types.addWidget(self.repeat_checkbox)
        self.event_types.addWidget(self.reminder_type)
        self.layout.addLayout(self.event_types)

        # -------- Alert & Skip Row --------
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

        # -------- Connections --------
        self.button_done.clicked.connect(self.save_event)
        self.button_cancel.clicked.connect(self.close)

        # -------- Load existing event --------
        self.load_selected_event()

    # ---------------- Load Event Data ----------------
    def load_selected_event(self):
        ev = self.event_data
        self.name_input.setText(ev.get("name", ""))
        self.event_input.setText(ev.get("event", ""))
        self.calendar.setSelectedDate(
            QtCore.QDate.fromString(ev.get("date", ""), "yyyy-MM-dd")
        )
        self.repeat_checkbox.setChecked(ev.get("repeat", "none") == "yearly")
        self.alert_days_spin.setValue(ev.get("alert", 0))

        # Reminder type
        rt = ev.get("reminder_type", "popup").capitalize()
        self.reminder_type.setCurrentText(rt)

        # Skip days
        skip_value = ev.get("skip", [])
        if isinstance(skip_value, int):
            skip_list = [skip_value]
        elif isinstance(skip_value, list):
            skip_list = skip_value
        else:
            skip_list = []
        self.skip_days.setText(",".join(str(n) for n in skip_list))

    # ---------------- Save Event Changes ----------------
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

        # Update the event data
        self.event_data.update({
            "name": name,
            "event": event,
            "date": date_str,
            "repeat": repeat_value,
            "reminder_type": reminder_type,
            "alert": alert_days,
            "skip": skip_list,
            "enabled": True,
        })

        save_data(self.file_path, self.data)
        self.event_saved.emit()
        self.close()