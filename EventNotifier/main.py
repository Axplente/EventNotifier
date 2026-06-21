import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import Window
from notifier import notifier_main


if __name__ == "__main__":
    if "--notify" in sys.argv:
        notifier_main()
    else:
        app = QApplication([])
        window = Window()
        window.show()
        sys.exit(app.exec())