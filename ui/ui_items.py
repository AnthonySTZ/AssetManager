from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from ui.ui_setups.ui_item_widget import Ui_Form as UiItemWidget
import os
import ressources_rc


class ItemWidget(QWidget):
    def __init__(self, item=None) -> None:
        super().__init__()
        self.ui = UiItemWidget()
        self.ui.setupUi(self)

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
        icon = QPixmap(f":/icons/ui/ressources/{icon_name}.png")
        self.ui.img_l.setPixmap(icon)

    def mouseReleaseEvent(self, event) -> None:
        if self.item is None:
            return
        print(self.item)
