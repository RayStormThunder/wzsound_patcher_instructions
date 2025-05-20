# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'convert.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog_Convert(object):
    def setupUi(self, Dialog_Convert):
        if not Dialog_Convert.objectName():
            Dialog_Convert.setObjectName(u"Dialog_Convert")
        Dialog_Convert.resize(600, 300)
        self.verticalLayout_4 = QVBoxLayout(Dialog_Convert)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(Dialog_Convert)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_3 = QFrame(Dialog_Convert)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.label_2)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.label_5)

        self.ConvertModified = QPushButton(self.frame_3)
        self.ConvertModified.setObjectName(u"ConvertModified")

        self.verticalLayout_7.addWidget(self.ConvertModified)

        self.verticalLayout_7.setStretch(1, 1)

        self.verticalLayout_3.addWidget(self.frame_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(Dialog_Convert)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label_3)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label_6)

        self.pushButton_3 = QPushButton(self.frame_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_6.addWidget(self.pushButton_3)

        self.verticalLayout_6.setStretch(1, 1)

        self.verticalLayout_2.addWidget(self.frame_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog_Convert)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.label_4)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.label_7)

        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout_5.addWidget(self.pushButton_4)

        self.verticalLayout_5.setStretch(1, 10)

        self.verticalLayout.addWidget(self.frame)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton(Dialog_Convert)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_4.addWidget(self.pushButton)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 2)

        self.retranslateUi(Dialog_Convert)

        QMetaObject.connectSlotsByName(Dialog_Convert)
    # setupUi

    def retranslateUi(self, Dialog_Convert):
        Dialog_Convert.setWindowTitle(QCoreApplication.translate("Dialog_Convert", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog_Convert", u"Pick one of the following options", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_Convert", u"Convert Modified WZSound to Project", None))
        self.label_5.setText(QCoreApplication.translate("Dialog_Convert", u"This button takes a WZSound that has already been edited and converts it into a Project. This will create a single instruction file for exporting the correct RWAV files, a BRWSD project, and a WZSound Patch Instructions folder", None))
        self.ConvertModified.setText(QCoreApplication.translate("Dialog_Convert", u"Convert WZSound to Project", None))
        self.label_3.setText(QCoreApplication.translate("Dialog_Convert", u"Patch to WZSound using Instructions", None))
        self.label_6.setText(QCoreApplication.translate("Dialog_Convert", u"This button will use this project's patch instructions to patch a WZSound, instead of having SSRando do it. Useful when working outside of rando. Can also be used in the following option if you want to convert it to a Switch WZSound", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog_Convert", u"Patch to WZSound", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_Convert", u"Patch WZSound to Switch WZSound", None))
        self.label_7.setText(QCoreApplication.translate("Dialog_Convert", u"This button takes a WZSound file that you already have patched and convert it to a Switch version of WZSound. THIS REQUIRES YOU TO HAVE A SWITCH VERSION OF WZSOUND", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog_Convert", u"Convert to Switch WZSound", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog_Convert", u"Close Window", None))
    # retranslateUi

