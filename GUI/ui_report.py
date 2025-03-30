# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QListView, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog_Report(object):
    def setupUi(self, Dialog_Report):
        if not Dialog_Report.objectName():
            Dialog_Report.setObjectName(u"Dialog_Report")
        Dialog_Report.resize(600, 300)
        self.verticalLayout = QVBoxLayout(Dialog_Report)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog_Report)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Dialog_Report)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(Dialog_Report)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(Dialog_Report)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(Dialog_Report)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_5)

        self.listView = QListView(Dialog_Report)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_6 = QLabel(Dialog_Report)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_6)

        self.listView_2 = QListView(Dialog_Report)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_3.addWidget(self.listView_2)

        self.button_reset = QPushButton(Dialog_Report)
        self.button_reset.setObjectName(u"button_reset")

        self.verticalLayout_3.addWidget(self.button_reset)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_explorer = QPushButton(Dialog_Report)
        self.button_explorer.setObjectName(u"button_explorer")

        self.horizontalLayout_2.addWidget(self.button_explorer)

        self.button_close = QPushButton(Dialog_Report)
        self.button_close.setObjectName(u"button_close")

        self.horizontalLayout_2.addWidget(self.button_close)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog_Report)

        QMetaObject.connectSlotsByName(Dialog_Report)
    # setupUi

    def retranslateUi(self, Dialog_Report):
        Dialog_Report.setWindowTitle(QCoreApplication.translate("Dialog_Report", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog_Report", u"Instruction file successfully created!", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_Report", u"Find it in your \"Releases\" folder", None))
        self.label_3.setText(QCoreApplication.translate("Dialog_Report", u"Inside your project folder should be \"WZSound_Patch_Instructions\"", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_Report", u"That entire folder is your output", None))
        self.label_5.setText(QCoreApplication.translate("Dialog_Report", u"Files that haven't changed", None))
        self.label_6.setText(QCoreApplication.translate("Dialog_Report", u"Files larger than original", None))
        self.button_reset.setText(QCoreApplication.translate("Dialog_Report", u"Reset Above Files in BRWSD Project", None))
        self.button_explorer.setText(QCoreApplication.translate("Dialog_Report", u"Open Release Project", None))
        self.button_close.setText(QCoreApplication.translate("Dialog_Report", u"Close Window", None))
    # retranslateUi

