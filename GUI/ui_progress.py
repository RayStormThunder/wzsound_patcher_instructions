# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog_Progress(object):
    def setupUi(self, Dialog_Progress):
        if not Dialog_Progress.objectName():
            Dialog_Progress.setObjectName(u"Dialog_Progress")
        Dialog_Progress.resize(200, 75)
        self.verticalLayout = QVBoxLayout(Dialog_Progress)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.generated_text = QLabel(Dialog_Progress)
        self.generated_text.setObjectName(u"generated_text")
        self.generated_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.generated_text)

        self.progressBar = QProgressBar(Dialog_Progress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_2.addWidget(self.progressBar)

        self.verticalLayout_2.setStretch(1, 5)

        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Dialog_Progress)

        QMetaObject.connectSlotsByName(Dialog_Progress)
    # setupUi

    def retranslateUi(self, Dialog_Progress):
        Dialog_Progress.setWindowTitle(QCoreApplication.translate("Dialog_Progress", u"Dialog", None))
        self.generated_text.setText(QCoreApplication.translate("Dialog_Progress", u"Working", None))
    # retranslateUi

