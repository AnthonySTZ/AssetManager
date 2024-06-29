from PySide2.QtWidgets import QWidget, QTextEdit, QComboBox, QPushButton, QMessageBox
from PySide2.QtGui import QPixmap
from maya_scripts.ui.ui_item_widget import Ui_Form as UiItemWidget
from bdd.database_handler import DatabaseHandler
import os
import ressources_maya_rc
import maya.cmds as cmds


class ItemWidget(QWidget):
    def __init__(self, database: DatabaseHandler, item=None) -> None:
        super().__init__()
        self.ui = UiItemWidget()
        self.ui.setupUi(self)
        self.database = database

        self.item = item
        self.init_texts()

    def init_texts(self) -> None:
        if self.item is None:
            return

        self.ui.type_l.setText(self.item["type"])
        self.ui.name_l.setText(self.item["name"])

        self.init_type()

    def init_type(self) -> None:
        if self.item["type"] == "Models":
            self.ui.type_l.setStyleSheet("background-color: rgb(100, 0, 0);")
            self.set_icon("model")
        elif self.item["type"] == "Materials":
            self.ui.type_l.setStyleSheet("background-color: rgb(0, 100, 0);")
            self.set_icon("material")
        else:
            self.ui.type_l.setStyleSheet("background-color: rgb(0, 0, 100);")
            self.set_icon("texture")

    def set_icon(self, icon_name) -> None:
        if "path" in self.item:
            if not os.path.exists(self.item["path"]):
                icon_name = "error"
        icon = QPixmap(":/icons/ui/ressources/" + icon_name + ".png")
        self.ui.img_l.setPixmap(icon)

    def normal_import(self) -> None:
        obj = cmds.file(self.item["path"], i=True, namespace=":")
        if self.item["material_id"] is None:
            return

    def import_as_reference(self) -> None:
        pass

    def mouseReleaseEvent(self, event) -> None:
        if self.item is None:
            return

        if self.item["type"] == "Models":
            if not os.path.exists(self.item["path"]):
                print("Asset not found")
                return

            print("Import Asset")
            import_message = QMessageBox()
            import_message.setWindowTitle("Import as")
            import_message.setText("Import : " + self.item["name"])
            import_message.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            import_message.button(QMessageBox.Yes).setText("Import")
            import_message.button(QMessageBox.No).setText("Import as reference")
            import_as = (
                import_message.exec_()
            )  # Yes : normal import, No : import as reference, Cancel: cancel import

            if import_as == QMessageBox.Cancel:
                print("Import aborted")
                return

            if import_as == QMessageBox.Yes:  # Normal import
                self.normal_import()
                return

            if import_as == QMessageBox.No:  # reference import
                self.import_as_reference()
                return
