# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import ressources_maya_rc


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(200, 250)
        Form.setMinimumSize(QSize(200, 250))
        Form.setMaximumSize(QSize(200, 250))
        Form.setMouseTracking(False)
        Form.setStyleSheet("")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.frame = QFrame(Form)
        self.frame.setObjectName("frame")
        self.frame.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame.setMouseTracking(True)
        self.frame.setStyleSheet(
            ".QLabel{\n"
            "	color: rgb(246, 245, 244);\n"
            "}\n"
            ".QFrame{\n"
            "	border: 2px solid rgb(100, 100, 100);\n"
            "	background-color: rgb(36, 36, 36);\n"
            "\n"
            "}\n"
            ".QFrame:hover{\n"
            "	border: 2px solid rgb(255, 190, 111);\n"
            "}\n"
            ""
        )
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(0)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.img_l = QLabel(self.frame)
        self.img_l.setObjectName("img_l")
        self.img_l.setPixmap(QPixmap(":/icons/ui/ressources/model.png"))
        self.img_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.img_l, 1, 0, 1, 1)

        self.name_l = QLabel(self.frame)
        self.name_l.setObjectName("name_l")
        self.name_l.setMaximumSize(QSize(16777215, 25))
        self.name_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.name_l, 2, 0, 1, 1)

        self.type_l = QLabel(self.frame)
        self.type_l.setObjectName("type_l")
        self.type_l.setMaximumSize(QSize(16777215, 25))
        self.type_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.type_l, 0, 0, 1, 1)

        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.img_l.setText("")
        self.name_l.setText(QCoreApplication.translate("Form", "Name", None))
        self.type_l.setText(QCoreApplication.translate("Form", "Type", None))

    # retranslateUi
