"""
Scripts for Handling all UI elements
"""

from PySide6.QtWidgets import QMainWindow, QDialog, QTextEdit, QPushButton, QComboBox
from ui.ui_manager_window import Ui_MainWindow
from ui.ui_import_asset import Ui_Dialog as UiImportAssetDialog
from ui.ui_import_texture import Ui_Dialog as UiImportTextureDialog


class DialogTemplate(QDialog):
    def __init__(self, ui, parent=None) -> None:
        super().__init__(parent)
        self.ui = ui()
        self.ui.setupUi(self)

        self.status = False
        self.init_buttons()

    def init_buttons(self) -> None:
        self.ui.accept_btn.clicked.connect(self.accept_event)
        self.ui.cancel_btn.clicked.connect(self.cancel_event)

    def everything_is_correct(self) -> bool:
        return False

    def accept_event(self) -> None:
        if not self.everything_is_correct():
            return
        self.status = True
        self.close()

    def cancel_event(self) -> None:
        self.close()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_buttons()

    def init_buttons(self) -> None:
        self.ui.asset_btn.clicked.connect(self.import_asset_event)
        self.ui.texture_btn.clicked.connect(self.import_texture_event)
        self.ui.material_btn.clicked.connect(self.create_material_event)
        self.ui.link_btn.clicked.connect(self.link_material_event)

    def import_asset_event(self) -> None:
        print("import asset !!!!")
        self.show_dialog(ImportAssetDialog)

    def import_texture_event(self) -> None:
        print("import texture !!!!")
        self.show_dialog(ImportTextureDialog)

    def create_material_event(self) -> None:
        print("create material !!!!")

    def link_material_event(self) -> None:
        print("link material !!!!")

    def show_dialog(self, dialog_class: DialogTemplate) -> dict:
        dialog = dialog_class(self)
        dialog.exec()
        if dialog.status != True:  # Return Empty dict if Dialog cancel or close
            return {}

        objects_dict = {}
        labels = dialog.findChildren(QTextEdit)
        for obj in labels:
            objects_dict[obj.objectName()] = obj.toPlainText()

        comboboxes = dialog.findChildren(QComboBox)
        for obj in comboboxes:
            objects_dict[obj.objectName()] = obj.currentIndex()

        print(objects_dict)

        return objects_dict


class ImportAssetDialog(DialogTemplate):
    def __init__(self, parent=None) -> None:
        super().__init__(UiImportAssetDialog, parent)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        return True


class ImportTextureDialog(DialogTemplate):
    def __init__(self, parent=None) -> None:
        super().__init__(UiImportTextureDialog, parent)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        return True
