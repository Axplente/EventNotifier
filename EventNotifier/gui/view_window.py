from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from gui.edit_window import EditWindow
from storage import save_data
from config import ICON_PATH

class ViewWindow(QtWidgets.QWidget):
    def __init__(self, data, file_path):
        super().__init__()
        self.setWindowTitle("Saved Events")
        self.setWindowIcon(QIcon(ICON_PATH))

        self.data = data
        self.file_path = file_path
        self.layout = QtWidgets.QVBoxLayout(self)

        # ---------------- List Widget ----------------
        self.list_widget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.list_widget)

        # ---------------- Buttons ----------------
        self.event_state_btn = QtWidgets.QPushButton("Toggle Event Status")
        self.edit_btn = QtWidgets.QPushButton("Edit Selected Event")
        self.delete_btn = QtWidgets.QPushButton("Delete Selected Event")
        self.close_btn = QtWidgets.QPushButton("Close")

        # Side-by-side layout
        top_buttons = QtWidgets.QHBoxLayout()
        top_buttons.addWidget(self.event_state_btn)
        top_buttons.addWidget(self.edit_btn)

        bottom_buttons = QtWidgets.QHBoxLayout()
        bottom_buttons.addWidget(self.delete_btn)
        bottom_buttons.addWidget(self.close_btn)

        self.layout.addLayout(top_buttons)
        self.layout.addLayout(bottom_buttons)

        # Disable buttons initially
        self.event_state_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        # ---------------- Connections ----------------
        self.list_widget.itemSelectionChanged.connect(self.update_buttons)
        self.list_widget.itemDoubleClicked.connect(self.open_edit_window)
        self.event_state_btn.clicked.connect(self.toggle_selected_event)
        self.edit_btn.clicked.connect(self.open_edit_window)
        self.delete_btn.clicked.connect(self.delete_event)
        self.close_btn.clicked.connect(self.close)

        self.populate_list()

    # ---------------- Populate List ----------------
    def populate_list(self):
        self.list_widget.clear()
        events = self.data.get("events", [])
        if not events:
            self.list_widget.addItem("No events saved yet.")
            return

        for event in events:
            status = "[Enabled]" if event.get("enabled", True) else "[Disabled]"
            self.list_widget.addItem(f"{event['date']} | {event['name']} | {event['event']} {status}")

    # ---------------- Update Buttons ----------------
    def update_buttons(self):
        events_exist = bool(self.data.get("events"))
        has_selection = bool(self.list_widget.selectedItems()) and events_exist
        self.event_state_btn.setEnabled(has_selection)
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    # ---------------- Toggle Status ----------------
    def toggle_selected_event(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.data.get("events", [])):
            return
        event = self.data["events"][row]
        event["enabled"] = not event.get("enabled", True)
        save_data(self.file_path, self.data)
        self.populate_list()
        self.update_buttons()

    # ---------------- Delete Event ----------------
    def delete_event(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.data.get("events", [])):
            return
        del self.data["events"][row]
        save_data(self.file_path, self.data)
        self.populate_list()
        self.update_buttons()

    # ---------------- Open Edit Window ----------------
    def open_edit_window(self, itme=None):
        row = self.list_widget.currentRow()
        if row == -1:
            return
        
        selected_event = self.data["events"][row]

        # keep a reference so delete_event can close it
        self.edit_window = EditWindow(self.data, self.file_path, selected_event)
        self.edit_window.event_saved.connect(self.populate_list)
        self.edit_window.load_selected_event()
        self.edit_window.show()

    def closeEvent(self, event):
        if hasattr(self, "edit_window") and self.edit_window is not None and self.edit_window.isVisible():
            self.edit_window.close()
        super().closeEvent(event)