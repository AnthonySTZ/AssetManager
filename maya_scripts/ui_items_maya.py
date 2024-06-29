from PySide2.QtWidgets import QWidget, QTextEdit, QComboBox, QPushButton, QMessageBox
from PySide2.QtGui import QPixmap
from maya_scripts.ui.ui_item_widget import Ui_Form as UiItemWidget
from bdd.database_handler import DatabaseHandler
import os
import ressources_maya_rc
import maya.cmds as cmds
import maya.mel as mel


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
        obj = cmds.file(
            self.item["path"], i=True, f=True, namespace=":"
        )  ####### obj = NONE pour fbx tant que l'utilisateur n'accepte pas le popup..... relou
        print(obj)
        if self.item["material_id"] is None:
            return

        material_info = self.database.get_item_of_table_by_id(
            "Materials", self.item["material_id"]
        )

        shader = self.create_material(material_info)
        self.assign_material(obj, shader)

    def import_as_reference(self) -> None:
        pass

    def create_file_texture(self, file_texture_name):
        tex = cmds.shadingNode(
            "file", name=file_texture_name, asTexture=True, isColorManaged=True
        )
        place_2d = cmds.shadingNode("place2dTexture", asUtility=True)
        cmds.connectAttr(place_2d + ".outUV", tex + ".uvCoord")
        cmds.connectAttr(place_2d + ".outUvFilterSize", tex + ".uvFilterSize")
        cmds.connectAttr(place_2d + ".vertexCameraOne", tex + ".vertexCameraOne")
        cmds.connectAttr(place_2d + ".vertexUvOne", tex + ".vertexUvOne")
        cmds.connectAttr(place_2d + ".vertexUvThree", tex + ".vertexUvThree")
        cmds.connectAttr(place_2d + ".vertexUvTwo", tex + ".vertexUvTwo")
        cmds.connectAttr(place_2d + ".coverage", tex + ".coverage")
        cmds.connectAttr(place_2d + ".mirrorU", tex + ".mirrorU")
        cmds.connectAttr(place_2d + ".mirrorV", tex + ".mirrorV")
        cmds.connectAttr(place_2d + ".noiseUV", tex + ".noiseUV")
        cmds.connectAttr(place_2d + ".offset", tex + ".offset")
        cmds.connectAttr(place_2d + ".repeatUV", tex + ".repeatUV")
        cmds.connectAttr(place_2d + ".rotateFrame", tex + ".rotateFrame")
        cmds.connectAttr(place_2d + ".rotateUV", tex + ".rotateUV")
        cmds.connectAttr(place_2d + ".stagger", tex + ".stagger")
        cmds.connectAttr(place_2d + ".translateFrame", tex + ".translateFrame")
        cmds.connectAttr(place_2d + ".wrapU", tex + ".wrapU")
        cmds.connectAttr(place_2d + ".wrapV", tex + ".wrapV")
        return tex

    def create_material(self, mat_infos=None) -> str:
        material = cmds.shadingNode(
            "aiStandardSurface", asShader=True, name=self.item["name"]
        )
        shading_engine = cmds.sets(
            name=material + "SG", empty=True, renderable=True, noSurfaceShader=True
        )
        cmds.connectAttr(material + ".outColor", shading_engine + ".surfaceShader")

        if mat_infos is None:
            return shading_engine

        if mat_infos["diffuse_id"] is None:
            return shading_engine
        else:
            diffuse_texture = self.create_file_texture(
                "diffuse_" + self.item["name"] + "_texture"
            )
            cmds.connectAttr(diffuse_texture + ".outColor", material + ".baseColor")

        return shading_engine

    def assign_material(self, objects, shaderSG) -> None:
        if objects:
            cmds.sets(objects, e=True, forceElement=shaderSG)

    def import_asset_dialog(self) -> None:
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

    def import_material_dialog(self, objects) -> None:
        import_message = QMessageBox()
        import_message.setWindowTitle("Import Material")
        import_message.setText("Import : " + self.item["name"])
        import_message.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        import_message.button(QMessageBox.Yes).setText("Import")
        import_message.button(QMessageBox.No).setText(
            "Import and assign to selected objects"
        )
        import_as = (
            import_message.exec_()
        )  # Yes : normal import, No : import as reference, Cancel: cancel import

        if import_as == QMessageBox.Cancel:
            print("Import aborted")
            return

        if import_as == QMessageBox.Yes:  # Normal import
            self.create_material()
            return

        if import_as == QMessageBox.No:  # import and assign
            shaderSG = self.create_material()
            self.assign_material(objects, shaderSG)
            return

    def mouseReleaseEvent(self, event) -> None:
        if self.item is None:
            return

        if self.item["type"] == "Models":
            if not os.path.exists(self.item["path"]):
                print("Asset not found")
                return

            print("Import Asset")
            self.import_asset_dialog()
            return

        if self.item["type"] == "Materials":
            print("Import Material")
            obj_selected = cmds.ls(sl=True, l=True)  # Get selected objects
            self.import_material_dialog(obj_selected)
            return
