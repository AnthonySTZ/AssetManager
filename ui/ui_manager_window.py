# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manager_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QPushButton, QScrollBar, QSizePolicy, QSpacerItem,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1123, 602)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.link_btn = QPushButton(self.centralwidget)
        self.link_btn.setObjectName(u"link_btn")

        self.gridLayout_2.addWidget(self.link_btn, 0, 3, 1, 1)

        self.texture_btn = QPushButton(self.centralwidget)
        self.texture_btn.setObjectName(u"texture_btn")

        self.gridLayout_2.addWidget(self.texture_btn, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.asset_btn = QPushButton(self.centralwidget)
        self.asset_btn.setObjectName(u"asset_btn")

        self.gridLayout_2.addWidget(self.asset_btn, 0, 0, 1, 1)

        self.material_btn = QPushButton(self.centralwidget)
        self.material_btn.setObjectName(u"material_btn")

        self.gridLayout_2.addWidget(self.material_btn, 0, 2, 1, 1)

        self.search_te = QTextEdit(self.centralwidget)
        self.search_te.setObjectName(u"search_te")
        self.search_te.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.search_te, 0, 5, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalScrollBar = QScrollBar(self.widget)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout.addWidget(self.verticalScrollBar)


        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 6)

        self.gridLayout_2.setRowStretch(2, 1)

        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.link_btn.setText(QCoreApplication.translate("MainWindow", u"Link Material", None))
        self.texture_btn.setText(QCoreApplication.translate("MainWindow", u"Import Texture", None))
        self.asset_btn.setText(QCoreApplication.translate("MainWindow", u"Import Asset", None))
        self.material_btn.setText(QCoreApplication.translate("MainWindow", u"Create Material", None))
    # retranslateUi

