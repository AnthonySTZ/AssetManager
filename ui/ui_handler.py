"""
Scripts for Handling all UI elements
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QTextEdit,
    QComboBox,
    QWidget,
    QListWidgetItem,
    QListWidget,
    QAbstractItemView,
)
from ui.ui_manager_window import Ui_MainWindow
from ui.ui_import_asset import Ui_Dialog as UiImportAssetDialog
from ui.ui_import_texture import Ui_Dialog as UiImportTextureDialog
from ui.ui_create_material import Ui_Dialog as UiCreateMaterialDialog
from ui.ui_item_widget import Ui_Form as UiItemWidget


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


class ItemWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = UiItemWidget()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_buttons()
        self.show()
        self.items = [
            "item_1",
            "item_2",
            "item_3",
            "item_4",
            "item_5",
            "item_6",
            "item_7",
            "item_8",
        ]

        self.add_all_items()

    def init_buttons(self) -> None:
        self.ui.asset_btn.clicked.connect(self.import_asset_event)
        self.ui.texture_btn.clicked.connect(self.import_texture_event)
        self.ui.material_btn.clicked.connect(self.create_material_event)
        self.ui.link_btn.clicked.connect(self.link_material_event)

    def import_asset_event(self) -> None:
        print("import asset !!!!")
        infos = self.show_dialog(ImportAssetDialog)
        print(infos)

    def import_texture_event(self) -> None:
        print("import texture !!!!")
        infos = self.show_dialog(ImportTextureDialog)
        print(infos)

    def create_material_event(self) -> None:
        print("create material !!!!")
        infos = self.show_dialog(CreateMaterialDialog)
        print(infos)

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

        return objects_dict

    def add_item_to_listWidget(self, list_widget, widget) -> None:
        item = QListWidgetItem(list_widget)
        item.setSizeHint(widget.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

    def add_item_row(self) -> None:
        list_widget = QListWidget()
        list_widget.setFlow(QListWidget.LeftToRight)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        list_widget.setFixedSize(self.ui.items_lw.width(), ItemWidget().height() + 10)
        self.add_item_to_listWidget(self.ui.items_lw, list_widget)

    def is_item_row_full(self):

        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        last_row = self.ui.items_lw.itemWidget(last_row_item)
        last_row_item_nb = last_row.count()
        widget_width = ItemWidget().width()
        return (last_row_item_nb + 1) * widget_width > self.ui.items_lw.width()

    def add_item(self) -> None:
        if self.ui.items_lw.count() == 0:
            self.add_item_row()

        elif self.is_item_row_full():
            self.add_item_row()

        item_widget = ItemWidget()
        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        self.add_item_to_listWidget(
            self.ui.items_lw.itemWidget(last_row_item), item_widget
        )

    def add_all_items(self) -> None:
        for item in self.items:
            self.add_item()

    def clear_all_items(self) -> None:
        self.ui.items_lw.clear()
        self.add_all_items()

    def resizeEvent(self, event) -> None:
        print(self.ui.items_lw.width())
        QMainWindow.resizeEvent(self, event)
        try:  # Check if resize is called before the window is created
            self.clear_all_items()
        except AttributeError:
            pass


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


class CreateMaterialDialog(DialogTemplate):
    def __init__(self, parent=None) -> None:
        super().__init__(UiCreateMaterialDialog, parent)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        return True
