# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_texture.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QTextEdit,
    QWidget)
import ressources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.path_te = QTextEdit(Dialog)
        self.path_te.setObjectName(u"path_te")
        self.path_te.setMaximumSize(QSize(16777215, 28))
        self.path_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.path_te.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.path_te.setLineWrapMode(QTextEdit.NoWrap)

        self.gridLayout.addWidget(self.path_te, 1, 1, 1, 2)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.cancel_btn = QPushButton(Dialog)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.gridLayout.addWidget(self.cancel_btn, 2, 0, 1, 2)

        self.file_btn = QPushButton(Dialog)
        self.file_btn.setObjectName(u"file_btn")
        self.file_btn.setMaximumSize(QSize(28, 28))
        self.file_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.file_btn.setStyleSheet(u"QPushButton{\n"
"	background: transparent;\n"
"\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/ui/ressources/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.file_btn.setIcon(icon)
        self.file_btn.setIconSize(QSize(28, 28))
        self.file_btn.setFlat(True)

        self.gridLayout.addWidget(self.file_btn, 1, 3, 1, 1)

        self.name_te = QTextEdit(Dialog)
        self.name_te.setObjectName(u"name_te")
        self.name_te.setMaximumSize(QSize(16777215, 28))
        self.name_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.name_te.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout.addWidget(self.name_te, 0, 1, 1, 3)

        self.accept_btn = QPushButton(Dialog)
        self.accept_btn.setObjectName(u"accept_btn")

        self.gridLayout.addWidget(self.accept_btn, 2, 2, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Name :", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Path :", None))
        self.cancel_btn.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.file_btn.setText("")
        self.accept_btn.setText(QCoreApplication.translate("Dialog", u"Accept", None))
    # retranslateUi

