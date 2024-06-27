import sys
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
import maya.api.OpenMaya as om


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SimpleWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)

        self.setWindowTitle("Simple PySide6 Window")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Hello, Maya!")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


def show_simple_window():
    global simple_window
    try:
        simple_window.close()  # Ferme la fenêtre existante si elle est ouverte
        simple_window.deleteLater()
    except:
        pass

    simple_window = SimpleWindow(parent=get_maya_main_window())
    simple_window.show()


def maya_useNewAPI():
    pass


def initializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.registerCommand("showSimpleWindow", show_simple_window)
        om.MGlobal.displayInfo("Simple PySide6 Plugin loaded!")
    except:
        om.MGlobal.displayError("Failed to register command: showSimpleWindow")


def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand("showSimpleWindow")
        om.MGlobal.displayInfo("Simple PySide6 Plugin unloaded!")
    except:
        om.MGlobal.displayError("Failed to deregister command: showSimpleWindow")
