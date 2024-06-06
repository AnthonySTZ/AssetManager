# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_material.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.normal_cb = QComboBox(Dialog)
        self.normal_cb.addItem("")
        self.normal_cb.setObjectName(u"normal_cb")

        self.gridLayout.addWidget(self.normal_cb, 4, 2, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.diffuse_cb = QComboBox(Dialog)
        self.diffuse_cb.addItem("")
        self.diffuse_cb.setObjectName(u"diffuse_cb")

        self.gridLayout.addWidget(self.diffuse_cb, 1, 2, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.specular_cb = QComboBox(Dialog)
        self.specular_cb.addItem("")
        self.specular_cb.setObjectName(u"specular_cb")

        self.gridLayout.addWidget(self.specular_cb, 2, 2, 1, 1)

        self.roughness_cb = QComboBox(Dialog)
        self.roughness_cb.addItem("")
        self.roughness_cb.setObjectName(u"roughness_cb")

        self.gridLayout.addWidget(self.roughness_cb, 3, 2, 1, 1)

        self.displacement_cb = QComboBox(Dialog)
        self.displacement_cb.addItem("")
        self.displacement_cb.setObjectName(u"displacement_cb")

        self.gridLayout.addWidget(self.displacement_cb, 5, 2, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.cancel_btn = QPushButton(Dialog)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.gridLayout.addWidget(self.cancel_btn, 6, 0, 1, 1)

        self.accept_btn = QPushButton(Dialog)
        self.accept_btn.setObjectName(u"accept_btn")

        self.gridLayout.addWidget(self.accept_btn, 6, 2, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.name_te = QTextEdit(Dialog)
        self.name_te.setObjectName(u"name_te")

        self.gridLayout.addWidget(self.name_te, 0, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.normal_cb.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Diffuse :", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Roughness :", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Displacement :", None))
        self.diffuse_cb.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Normal :", None))
        self.specular_cb.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))

        self.roughness_cb.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))

        self.displacement_cb.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Specular :", None))
        self.cancel_btn.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.accept_btn.setText(QCoreApplication.translate("Dialog", u"Accept", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Name :", None))
    # retranslateUi

