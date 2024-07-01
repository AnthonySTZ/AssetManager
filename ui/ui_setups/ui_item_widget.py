# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QWidget)
import ressources_rc
import ressources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(200, 250)
        Form.setMinimumSize(QSize(200, 250))
        Form.setMaximumSize(QSize(200, 250))
        Form.setMouseTracking(False)
        Form.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame.setMouseTracking(True)
        self.frame.setStyleSheet(u".QLabel{\n"
"	color: rgb(246, 245, 244);\n"
"}\n"
".QFrame{\n"
"	background-color: rgb(32, 32, 32);\n"
"	margin: 2px;\n"
"	padding: 0px\n"
"}\n"
".QFrame:hover{\n"
"	border: 2px outset rgb(100, 100, 100);\n"
"	border-radius: 10px;\n"
"	margin: 0px;\n"
"	padding: 2px;\n"
"}\n"
"")
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(0)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.img_l = QLabel(self.frame)
        self.img_l.setObjectName(u"img_l")
        self.img_l.setFrameShadow(QFrame.Sunken)
        self.img_l.setLineWidth(1)
        self.img_l.setMidLineWidth(0)
        self.img_l.setPixmap(QPixmap(u":/icons/ui/ressources/error.png"))
        self.img_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.img_l, 1, 0, 1, 1)

        self.name_l = QLabel(self.frame)
        self.name_l.setObjectName(u"name_l")
        self.name_l.setMinimumSize(QSize(0, 25))
        self.name_l.setMaximumSize(QSize(16777215, 25))
        self.name_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.name_l, 2, 0, 1, 1)

        self.type_l = QLabel(self.frame)
        self.type_l.setObjectName(u"type_l")
        self.type_l.setMinimumSize(QSize(0, 25))
        self.type_l.setMaximumSize(QSize(16777215, 25))
        self.type_l.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.type_l, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.img_l.setText("")
        self.name_l.setText(QCoreApplication.translate("Form", u"Name", None))
        self.type_l.setText(QCoreApplication.translate("Form", u"Type", None))
    # retranslateUi

