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

    def import_fbx(self) -> list:
        obj_list = []
        all_old_obj = cmds.ls()
        import_status = mel.eval('FBXImport -f "' + self.item["path"] + '"')
        if import_status == "Success":
            all_obj = cmds.ls()
            for obj_name in all_obj:
                if obj_name not in all_old_obj:
                    obj_list.append(obj_name)
        return obj_list

    def normal_import(self) -> None:
        if self.item["path"].endswith(".fbx"):
            obj = self.import_fbx()
        else:
            obj = cmds.file(self.item["path"], i=True, namespace=":")
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

    def create_texture(
        self,
        textureType,
        texture_id,
        material,
        connectAttribute,
        non_color,
        colorSpace=None,
        is_normal=False,
        is_disp=False,
        shader=None,
    ):
        texture = self.create_file_texture(
            textureType + "_" + self.item["name"] + "_texture"
        )
        if not is_disp:
            if not is_normal:
                if non_color:
                    cmds.connectAttr(
                        texture + ".outColorR", material + "." + connectAttribute
                    )
                else:
                    cmds.connectAttr(
                        texture + ".outColor", material + "." + connectAttribute
                    )
            else:  # Set Normal Node for normal map
                normalmap_node = cmds.shadingNode("aiNormalMap", asTexture=True)
                cmds.connectAttr(texture + ".outColor", normalmap_node + ".input")
                cmds.connectAttr(
                    normalmap_node + ".outValue", material + ".normalCamera"
                )
        else:  # Set Displacement Node for disp map
            displacement_node = cmds.shadingNode("displacementShader", asShader=True)
            cmds.connectAttr(
                texture + ".outColorR", displacement_node + ".displacement"
            )
            cmds.connectAttr(
                displacement_node + ".displacement", shader + ".displacementShader"
            )

        texture_infos = self.database.get_item_of_table_by_id("Textures", texture_id)
        cmds.setAttr(
            texture + ".fileTextureName",
            texture_infos["path"],
            type="string",
        )

        if colorSpace is not None:
            cmds.setAttr(texture + ".colorSpace", colorSpace, type="string")

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

        if mat_infos["diffuse_id"] is not None:
            self.create_texture(
                "diffuse", mat_infos["diffuse_id"], material, "baseColor", False
            )

        if mat_infos["specular_id"] is not None:
            self.create_texture(
                "specular", mat_infos["specular_id"], material, "specular", True, "Raw"
            )

        if mat_infos["roughness_id"] is not None:
            self.create_texture(
                "roughness",
                mat_infos["roughness_id"],
                material,
                "specularRoughness",
                True,
                "Raw",
            )

        if mat_infos["metalness_id"] is not None:
            self.create_texture(
                "metalness",
                mat_infos["metalness_id"],
                material,
                "metalness",
                True,
                "Raw",
            )

        if mat_infos["normal_id"] is not None:
            self.create_texture(
                "normal",
                mat_infos["normal_id"],
                material,
                "normal",
                False,
                "Raw",
                True,
            )

        if mat_infos["displacement_id"] is not None:
            self.create_texture(
                "displacement",
                mat_infos["displacement_id"],
                material,
                "displacement",
                False,
                "Raw",
                False,
                True,
                shading_engine,
            )

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
            material_info = self.database.get_item_of_table_by_id(
                "Materials", self.item["id"]
            )
            self.create_material(material_info)
            return

        if import_as == QMessageBox.No:  # import and assign
            material_info = self.database.get_item_of_table_by_id(
                "Materials", self.item["id"]
            )
            shaderSG = self.create_material(material_info)
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
