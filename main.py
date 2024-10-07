"""
Main Scripts, launch Qt UI
"""

import sys
from PySide6.QtWidgets import QApplication
import ui.ui_handler as ui
import renderer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ui.MainWindow()

    sys.exit(app.exec())
