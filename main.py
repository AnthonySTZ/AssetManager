"""
Main Scripts, launch Qt UI
"""

"""A:/Programming/AssetManager/test_files/models/historical/vkubdea_2K_Albedo.jpg"""

import sys
from PySide6.QtWidgets import QApplication
import ui.ui_handler as ui

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ui.MainWindow()

    sys.exit(app.exec())
