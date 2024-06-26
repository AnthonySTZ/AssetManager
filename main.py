"""
Main Scripts, launch Qt UI
"""

import sys
from PySide6.QtWidgets import QApplication
import ui.main_ui_handler as ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ui.MainWindow()

    sys.exit(app.exec())
