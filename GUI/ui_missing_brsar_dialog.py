# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'missing_brsar_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(260, 100)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_error = QLabel(Dialog)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_error.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_error)

        self.button_error = QPushButton(Dialog)
        self.button_error.setObjectName(u"button_error")

        self.verticalLayout.addWidget(self.button_error)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_error.setText(QCoreApplication.translate("Dialog", u"You don't have an SD WZSound.brsar imported. Please import an unmodified Skyward Sword SD WZSound.brsar!", None))
        self.button_error.setText(QCoreApplication.translate("Dialog", u"Import WZSound.brsar", None))
    # retranslateUi

