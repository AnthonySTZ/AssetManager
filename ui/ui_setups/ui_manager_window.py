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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)
import ressources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1060, 700)
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"	background-color: rgb(40, 40, 40);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.search_te = QTextEdit(self.centralwidget)
        self.search_te.setObjectName(u"search_te")
        self.search_te.setMinimumSize(QSize(350, 0))
        self.search_te.setMaximumSize(QSize(350, 30))
        self.search_te.setStyleSheet(u"QTextEdit {\n"
"\n"
"	color: rgb(246, 245, 244);\n"
"	background-color: rgb(52, 52, 52);\n"
"	border : 1px solid grey;\n"
"	border-radius: 15px;\n"
"	padding-left : 8px;\n"
"	padding-top: 3px;\n"
"\n"
"}")
        self.search_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_te.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_2.addWidget(self.search_te, 0, 8, 1, 1)

        self.asset_btn = QPushButton(self.centralwidget)
        self.asset_btn.setObjectName(u"asset_btn")
        self.asset_btn.setMinimumSize(QSize(0, 0))
        self.asset_btn.setStyleSheet(u"QPushButton{\n"
"\n"
"	color: rgb(200, 200, 200);\n"
"	background-color: rgba(60, 60, 60, 0);\n"
"	border-radius: 3px;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	color: rgb(220, 220, 220);\n"
"	background-color: rgba(60, 60, 60, 200);\n"
"}")
        self.asset_btn.setFlat(False)

        self.gridLayout_2.addWidget(self.asset_btn, 0, 0, 1, 1)

        self.texture_btn = QPushButton(self.centralwidget)
        self.texture_btn.setObjectName(u"texture_btn")
        self.texture_btn.setStyleSheet(u"QPushButton{\n"
"\n"
"	color: rgb(200, 200, 200);\n"
"	background-color: rgba(60, 60, 60, 0);\n"
"	border-radius: 3px;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	color: rgb(220, 220, 220);\n"
"	background-color: rgba(60, 60, 60, 200);\n"
"}")

        self.gridLayout_2.addWidget(self.texture_btn, 0, 1, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.items_lw = QListWidget(self.widget)
        self.items_lw.setObjectName(u"items_lw")
        self.items_lw.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.items_lw.setMouseTracking(False)
        self.items_lw.setFocusPolicy(Qt.NoFocus)
        self.items_lw.setStyleSheet(u".QListWidget{\n"
"	border: 0;\n"
"	background: transparent;\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"	background: rgb(30, 30, 30);\n"
"	width:10px;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"	background-color: rgb(60, 60, 60);\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"\n"
"")
        self.items_lw.setFrameShape(QFrame.StyledPanel)
        self.items_lw.setFrameShadow(QFrame.Sunken)
        self.items_lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.items_lw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.items_lw.setAutoScroll(True)
        self.items_lw.setAutoScrollMargin(16)
        self.items_lw.setSelectionMode(QAbstractItemView.NoSelection)
        self.items_lw.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.items_lw.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.items_lw.setMovement(QListView.Free)
        self.items_lw.setViewMode(QListView.IconMode)

        self.horizontalLayout.addWidget(self.items_lw)


        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 9)

        self.material_btn = QPushButton(self.centralwidget)
        self.material_btn.setObjectName(u"material_btn")
        self.material_btn.setStyleSheet(u"QPushButton{\n"
"\n"
"	color: rgb(200, 200, 200);\n"
"	background-color: rgba(60, 60, 60, 0);\n"
"	border-radius: 3px;\n"
"	padding: 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	color: rgb(220, 220, 220);\n"
"	background-color: rgba(60, 60, 60, 200);\n"
"}")

        self.gridLayout_2.addWidget(self.material_btn, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 0))
        self.widget_2.setStyleSheet(u"QPushButton {\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"\n"
"background-color: rgb(25, 25, 25);\n"
"\n"
"}\n"
"")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.all_check = QPushButton(self.widget_2)
        self.all_check.setObjectName(u"all_check")
        icon = QIcon()
        icon.addFile(u":/icons/ui/ressources/all.png", QSize(), QIcon.Normal, QIcon.Off)
        self.all_check.setIcon(icon)
        self.all_check.setIconSize(QSize(20, 20))
        self.all_check.setCheckable(True)
        self.all_check.setChecked(True)
        self.all_check.setFlat(False)

        self.horizontalLayout_4.addWidget(self.all_check)

        self.models_check = QPushButton(self.widget_2)
        self.models_check.setObjectName(u"models_check")
        self.models_check.setCursor(QCursor(Qt.ArrowCursor))
        self.models_check.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/ressources/model.png", QSize(), QIcon.Normal, QIcon.Off)
        self.models_check.setIcon(icon1)
        self.models_check.setIconSize(QSize(20, 20))
        self.models_check.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.models_check)

        self.textures_check = QPushButton(self.widget_2)
        self.textures_check.setObjectName(u"textures_check")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/ressources/texture.png", QSize(), QIcon.Normal, QIcon.Off)
        self.textures_check.setIcon(icon2)
        self.textures_check.setIconSize(QSize(20, 20))
        self.textures_check.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.textures_check)

        self.materials_check = QPushButton(self.widget_2)
        self.materials_check.setObjectName(u"materials_check")
        icon3 = QIcon()
        icon3.addFile(u":/icons/ui/ressources/material.png", QSize(), QIcon.Normal, QIcon.Off)
        self.materials_check.setIcon(icon3)
        self.materials_check.setIconSize(QSize(20, 20))
        self.materials_check.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.materials_check)


        self.gridLayout_2.addWidget(self.widget_2, 0, 4, 1, 4)


        self.verticalLayout.addLayout(self.gridLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.asset_btn.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.search_te.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.asset_btn.setText(QCoreApplication.translate("MainWindow", u"Import Asset", None))
        self.texture_btn.setText(QCoreApplication.translate("MainWindow", u"Import Texture", None))
        self.material_btn.setText(QCoreApplication.translate("MainWindow", u"Create Material", None))
        self.all_check.setText("")
        self.models_check.setText("")
        self.textures_check.setText("")
        self.materials_check.setText("")
    # retranslateUi

