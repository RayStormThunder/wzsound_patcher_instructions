# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_WZSPI_MainWindow(object):
    def setupUi(self, WZSPI_MainWindow):
        if not WZSPI_MainWindow.objectName():
            WZSPI_MainWindow.setObjectName(u"WZSPI_MainWindow")
        WZSPI_MainWindow.resize(800, 600)
        self.centralwidget = QWidget(WZSPI_MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_5.addWidget(self.pushButton_9)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_5.addWidget(self.pushButton_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout.addWidget(self.listWidget)

        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_8)

        self.listWidget_2 = QListWidget(self.centralwidget)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.horizontalLayout.addWidget(self.listWidget_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_5 = QPushButton(self.frame)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_2.addWidget(self.pushButton_5)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_6 = QPushButton(self.frame_2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.frame_2)


        self.horizontalLayout_7.addLayout(self.verticalLayout)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_8.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_8.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_8.addWidget(self.pushButton_3)


        self.gridLayout.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        WZSPI_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(WZSPI_MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 43))
        self.menuWZ_Sound_Patcher_Instructions = QMenu(self.menubar)
        self.menuWZ_Sound_Patcher_Instructions.setObjectName(u"menuWZ_Sound_Patcher_Instructions")
        WZSPI_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(WZSPI_MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        WZSPI_MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuWZ_Sound_Patcher_Instructions.menuAction())

        self.retranslateUi(WZSPI_MainWindow)

        QMetaObject.connectSlotsByName(WZSPI_MainWindow)
    # setupUi

    def retranslateUi(self, WZSPI_MainWindow):
        WZSPI_MainWindow.setWindowTitle(QCoreApplication.translate("WZSPI_MainWindow", u"WZSPI_MainWindow", None))
        self.pushButton_9.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Instructions", None))
        self.pushButton_7.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Edit Instructions", None))
        self.pushButton_8.setText(QCoreApplication.translate("WZSPI_MainWindow", u"<-Move->", None))
        self.pushButton_5.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Project BRWSD", None))
        self.label.setText(QCoreApplication.translate("WZSPI_MainWindow", u"After setting up your instructions. You can click the \"Create Project BRWSD\" button. This will extract every RWAV that the instructions specified and combine them into a single BRWSD file. You can then open this file with Brawlcrate. Every RWAV you want to edit will be there. You can make changes in that file and save your changes.", None))
        self.pushButton_6.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create WZSound Patcher Instructions", None))
        self.label_2.setText(QCoreApplication.translate("WZSPI_MainWindow", u"I'm so frustrated with QT.", None))
        self.pushButton_2.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Project", None))
        self.pushButton.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load Project", None))
        self.pushButton_3.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Convert Project", None))
        self.menuWZ_Sound_Patcher_Instructions.setTitle(QCoreApplication.translate("WZSPI_MainWindow", u"WZ Sound Patcher Instructions", None))
    # retranslateUi

