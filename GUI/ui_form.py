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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QStackedWidget, QStatusBar, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_WZSPI_MainWindow(object):
    def setupUi(self, WZSPI_MainWindow):
        if not WZSPI_MainWindow.objectName():
            WZSPI_MainWindow.setObjectName(u"WZSPI_MainWindow")
        WZSPI_MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(WZSPI_MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.vertical_main = QVBoxLayout()
        self.vertical_main.setObjectName(u"vertical_main")
        self.horizontal_1_project_buttons = QHBoxLayout()
        self.horizontal_1_project_buttons.setObjectName(u"horizontal_1_project_buttons")
        self.button_create_project = QPushButton(self.centralwidget)
        self.button_create_project.setObjectName(u"button_create_project")

        self.horizontal_1_project_buttons.addWidget(self.button_create_project)

        self.button_load_project = QPushButton(self.centralwidget)
        self.button_load_project.setObjectName(u"button_load_project")

        self.horizontal_1_project_buttons.addWidget(self.button_load_project)

        self.button_convert_project = QPushButton(self.centralwidget)
        self.button_convert_project.setObjectName(u"button_convert_project")

        self.horizontal_1_project_buttons.addWidget(self.button_convert_project)


        self.vertical_main.addLayout(self.horizontal_1_project_buttons)

        self.horizontal_2_main_content = QHBoxLayout()
        self.horizontal_2_main_content.setSpacing(4)
        self.horizontal_2_main_content.setObjectName(u"horizontal_2_main_content")
        self.description_text = QTextBrowser(self.centralwidget)
        self.description_text.setObjectName(u"description_text")
        self.description_text.setMinimumSize(QSize(300, 0))
        self.description_text.setMaximumSize(QSize(300, 16777215))
        self.description_text.setReadOnly(True)

        self.horizontal_2_main_content.addWidget(self.description_text)

        self.stacked_pages = QStackedWidget(self.centralwidget)
        self.stacked_pages.setObjectName(u"stacked_pages")
        self.page_1_pick_instructions = QWidget()
        self.page_1_pick_instructions.setObjectName(u"page_1_pick_instructions")
        self.horizontalLayout_6 = QHBoxLayout(self.page_1_pick_instructions)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.vertical_pick = QVBoxLayout()
        self.vertical_pick.setObjectName(u"vertical_pick")
        self.frame_pick = QFrame(self.page_1_pick_instructions)
        self.frame_pick.setObjectName(u"frame_pick")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_pick.sizePolicy().hasHeightForWidth())
        self.frame_pick.setSizePolicy(sizePolicy)
        self.frame_pick.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pick.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_pick)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontal_instructions_buttons = QHBoxLayout()
        self.horizontal_instructions_buttons.setObjectName(u"horizontal_instructions_buttons")
        self.button_create_instructions = QPushButton(self.frame_pick)
        self.button_create_instructions.setObjectName(u"button_create_instructions")

        self.horizontal_instructions_buttons.addWidget(self.button_create_instructions)

        self.button_edit_instructions = QPushButton(self.frame_pick)
        self.button_edit_instructions.setObjectName(u"button_edit_instructions")

        self.horizontal_instructions_buttons.addWidget(self.button_edit_instructions)


        self.verticalLayout_6.addLayout(self.horizontal_instructions_buttons)

        self.horizontal_selector = QHBoxLayout()
        self.horizontal_selector.setObjectName(u"horizontal_selector")
        self.vertical_1_options_list = QVBoxLayout()
        self.vertical_1_options_list.setObjectName(u"vertical_1_options_list")
        self.frame_options = QFrame(self.frame_pick)
        self.frame_options.setObjectName(u"frame_options")
        self.frame_options.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_options.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_options)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_options = QLabel(self.frame_options)
        self.label_options.setObjectName(u"label_options")
        self.label_options.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_options)


        self.vertical_1_options_list.addWidget(self.frame_options)

        self.list_options = QListWidget(self.frame_pick)
        self.list_options.setObjectName(u"list_options")
        self.list_options.setDragEnabled(False)
        self.list_options.setAlternatingRowColors(True)
        self.list_options.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.vertical_1_options_list.addWidget(self.list_options)


        self.horizontal_selector.addLayout(self.vertical_1_options_list)

        self.vertical_2_move = QVBoxLayout()
        self.vertical_2_move.setObjectName(u"vertical_2_move")
        self.button_move = QPushButton(self.frame_pick)
        self.button_move.setObjectName(u"button_move")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_move.sizePolicy().hasHeightForWidth())
        self.button_move.setSizePolicy(sizePolicy1)

        self.vertical_2_move.addWidget(self.button_move)


        self.horizontal_selector.addLayout(self.vertical_2_move)

        self.vertical_3_project_list = QVBoxLayout()
        self.vertical_3_project_list.setObjectName(u"vertical_3_project_list")
        self.frame_project = QFrame(self.frame_pick)
        self.frame_project.setObjectName(u"frame_project")
        self.frame_project.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_project.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_project)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_project = QLabel(self.frame_project)
        self.label_project.setObjectName(u"label_project")
        self.label_project.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_project)


        self.vertical_3_project_list.addWidget(self.frame_project)

        self.list_project = QListWidget(self.frame_pick)
        self.list_project.setObjectName(u"list_project")
        self.list_project.setAlternatingRowColors(True)
        self.list_project.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.vertical_3_project_list.addWidget(self.list_project)


        self.horizontal_selector.addLayout(self.vertical_3_project_list)


        self.verticalLayout_6.addLayout(self.horizontal_selector)

        self.vertical_description = QVBoxLayout()
        self.vertical_description.setObjectName(u"vertical_description")

        self.verticalLayout_6.addLayout(self.vertical_description)


        self.vertical_pick.addWidget(self.frame_pick)


        self.horizontalLayout_6.addLayout(self.vertical_pick)

        self.stacked_pages.addWidget(self.page_1_pick_instructions)
        self.page_2_edit_instructions = QWidget()
        self.page_2_edit_instructions.setObjectName(u"page_2_edit_instructions")
        self.horizontalLayout_9 = QHBoxLayout(self.page_2_edit_instructions)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.vertical_edit = QVBoxLayout()
        self.vertical_edit.setObjectName(u"vertical_edit")
        self.frame_edit = QFrame(self.page_2_edit_instructions)
        self.frame_edit.setObjectName(u"frame_edit")
        self.frame_edit.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_edit.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_edit)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontal_changes_buttons = QHBoxLayout()
        self.horizontal_changes_buttons.setObjectName(u"horizontal_changes_buttons")
        self.button_save_changes = QPushButton(self.frame_edit)
        self.button_save_changes.setObjectName(u"button_save_changes")

        self.horizontal_changes_buttons.addWidget(self.button_save_changes)

        self.button_cancel_changes = QPushButton(self.frame_edit)
        self.button_cancel_changes.setObjectName(u"button_cancel_changes")

        self.horizontal_changes_buttons.addWidget(self.button_cancel_changes)


        self.verticalLayout_12.addLayout(self.horizontal_changes_buttons)

        self.text_yaml_edit = QTextEdit(self.frame_edit)
        self.text_yaml_edit.setObjectName(u"text_yaml_edit")
        self.text_yaml_edit.setTabStopDistance(10.000000000000000)

        self.verticalLayout_12.addWidget(self.text_yaml_edit)


        self.vertical_edit.addWidget(self.frame_edit)


        self.horizontalLayout_9.addLayout(self.vertical_edit)

        self.stacked_pages.addWidget(self.page_2_edit_instructions)

        self.horizontal_2_main_content.addWidget(self.stacked_pages)

        self.vertical_create = QVBoxLayout()
        self.vertical_create.setObjectName(u"vertical_create")
        self.frame_1_create_brwsd = QFrame(self.centralwidget)
        self.frame_1_create_brwsd.setObjectName(u"frame_1_create_brwsd")
        self.frame_1_create_brwsd.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1_create_brwsd.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_1_create_brwsd)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.buttons_brwsd = QHBoxLayout()
        self.buttons_brwsd.setObjectName(u"buttons_brwsd")
        self.button_create_brwsd = QPushButton(self.frame_1_create_brwsd)
        self.button_create_brwsd.setObjectName(u"button_create_brwsd")

        self.buttons_brwsd.addWidget(self.button_create_brwsd)

        self.button_load_brwsd_folder = QPushButton(self.frame_1_create_brwsd)
        self.button_load_brwsd_folder.setObjectName(u"button_load_brwsd_folder")

        self.buttons_brwsd.addWidget(self.button_load_brwsd_folder)


        self.verticalLayout_2.addLayout(self.buttons_brwsd)

        self.label_description_brwsd = QTextEdit(self.frame_1_create_brwsd)
        self.label_description_brwsd.setObjectName(u"label_description_brwsd")
        self.label_description_brwsd.setFrameShape(QFrame.Shape.NoFrame)
        self.label_description_brwsd.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.label_description_brwsd)


        self.vertical_create.addWidget(self.frame_1_create_brwsd)

        self.frame_2_create_wzsound = QFrame(self.centralwidget)
        self.frame_2_create_wzsound.setObjectName(u"frame_2_create_wzsound")
        self.frame_2_create_wzsound.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2_create_wzsound.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2_create_wzsound)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.button_instructions = QHBoxLayout()
        self.button_instructions.setObjectName(u"button_instructions")
        self.button_create_wzsound = QPushButton(self.frame_2_create_wzsound)
        self.button_create_wzsound.setObjectName(u"button_create_wzsound")

        self.button_instructions.addWidget(self.button_create_wzsound)

        self.button_load_instructions_folder = QPushButton(self.frame_2_create_wzsound)
        self.button_load_instructions_folder.setObjectName(u"button_load_instructions_folder")

        self.button_instructions.addWidget(self.button_load_instructions_folder)


        self.verticalLayout_3.addLayout(self.button_instructions)

        self.label_description_wzsound = QTextEdit(self.frame_2_create_wzsound)
        self.label_description_wzsound.setObjectName(u"label_description_wzsound")
        self.label_description_wzsound.setFrameShape(QFrame.Shape.NoFrame)
        self.label_description_wzsound.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.label_description_wzsound)


        self.vertical_create.addWidget(self.frame_2_create_wzsound)

        self.frame_4_create_wzsound_hd = QFrame(self.centralwidget)
        self.frame_4_create_wzsound_hd.setObjectName(u"frame_4_create_wzsound_hd")
        self.frame_4_create_wzsound_hd.setMinimumSize(QSize(0, 0))
        self.frame_4_create_wzsound_hd.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4_create_wzsound_hd.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_4_create_wzsound_hd)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttons_patcher = QHBoxLayout()
        self.buttons_patcher.setObjectName(u"buttons_patcher")
        self.buttons_patcher.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.patch_sd = QPushButton(self.frame_4_create_wzsound_hd)
        self.patch_sd.setObjectName(u"patch_sd")

        self.buttons_patcher.addWidget(self.patch_sd)

        self.load_sd = QPushButton(self.frame_4_create_wzsound_hd)
        self.load_sd.setObjectName(u"load_sd")

        self.buttons_patcher.addWidget(self.load_sd)


        self.verticalLayout.addLayout(self.buttons_patcher)

        self.label_description_patcher_hd = QTextEdit(self.frame_4_create_wzsound_hd)
        self.label_description_patcher_hd.setObjectName(u"label_description_patcher_hd")
        self.label_description_patcher_hd.setFrameShape(QFrame.Shape.NoFrame)
        self.label_description_patcher_hd.setReadOnly(True)

        self.verticalLayout.addWidget(self.label_description_patcher_hd)


        self.vertical_create.addWidget(self.frame_4_create_wzsound_hd)

        self.frame_3_patch_wzsound_sd = QFrame(self.centralwidget)
        self.frame_3_patch_wzsound_sd.setObjectName(u"frame_3_patch_wzsound_sd")
        self.frame_3_patch_wzsound_sd.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3_patch_wzsound_sd.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3_path_wzsound = QVBoxLayout(self.frame_3_patch_wzsound_sd)
        self.frame_3_path_wzsound.setSpacing(4)
        self.frame_3_path_wzsound.setObjectName(u"frame_3_path_wzsound")
        self.frame_3_path_wzsound.setContentsMargins(6, 6, 6, 6)
        self.button_load_patcher = QHBoxLayout()
        self.button_load_patcher.setObjectName(u"button_load_patcher")
        self.patch_hd = QPushButton(self.frame_3_patch_wzsound_sd)
        self.patch_hd.setObjectName(u"patch_hd")

        self.button_load_patcher.addWidget(self.patch_hd)

        self.load_hd = QPushButton(self.frame_3_patch_wzsound_sd)
        self.load_hd.setObjectName(u"load_hd")

        self.button_load_patcher.addWidget(self.load_hd)


        self.frame_3_path_wzsound.addLayout(self.button_load_patcher)

        self.label_description_patcher_sd = QTextEdit(self.frame_3_patch_wzsound_sd)
        self.label_description_patcher_sd.setObjectName(u"label_description_patcher_sd")
        self.label_description_patcher_sd.setFrameShape(QFrame.Shape.NoFrame)
        self.label_description_patcher_sd.setReadOnly(True)

        self.frame_3_path_wzsound.addWidget(self.label_description_patcher_sd)


        self.vertical_create.addWidget(self.frame_3_patch_wzsound_sd)

        self.vertical_create.setStretch(0, 1)
        self.vertical_create.setStretch(1, 1)
        self.vertical_create.setStretch(2, 1)
        self.vertical_create.setStretch(3, 1)

        self.horizontal_2_main_content.addLayout(self.vertical_create)

        self.horizontal_2_main_content.setStretch(1, 3)
        self.horizontal_2_main_content.setStretch(2, 1)

        self.vertical_main.addLayout(self.horizontal_2_main_content)


        self.gridLayout.addLayout(self.vertical_main, 2, 0, 1, 1)

        WZSPI_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(WZSPI_MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        WZSPI_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(WZSPI_MainWindow)

        self.stacked_pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(WZSPI_MainWindow)
    # setupUi

    def retranslateUi(self, WZSPI_MainWindow):
        WZSPI_MainWindow.setWindowTitle(QCoreApplication.translate("WZSPI_MainWindow", u"WZSPI_MainWindow", None))
        self.button_create_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u" Create SD Project", None))
        self.button_load_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load SD Project", None))
        self.button_convert_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Convert Modified SD WZSound to Project", None))
        self.button_create_instructions.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create RWAV Extraction Instructions", None))
        self.button_edit_instructions.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Edit RWAV Extraction Instructions", None))
        self.label_options.setText(QCoreApplication.translate("WZSPI_MainWindow", u"All Options", None))
        self.button_move.setText(QCoreApplication.translate("WZSPI_MainWindow", u"<-Move->", None))
        self.label_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"NO PROJECT LOADED", None))
        self.button_save_changes.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Save Changes", None))
        self.button_cancel_changes.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Cancel Changes", None))
        self.button_create_brwsd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create SD Project BRWSD", None))
        self.button_load_brwsd_folder.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load Project Folder", None))
        self.label_description_brwsd.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This creates a BRWSD file with every RWAV file extracted from your instructions. You will be able to edit it with Brawlcrate AND be able to save that file.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0p"
                        "x; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; font-style:italic; text-decoration: underline;\">Create SD Project BRWSD</span> Requirements:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Moved at least one instruction file to the right</p></body></html>", None))
        self.button_create_wzsound.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create SD WZSound Patcher Instructions", None))
        self.button_load_instructions_folder.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load Instructions Folder", None))
        self.label_description_wzsound.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Creates a folder that contains every modified RWAV from your Project BRWSD and a file that records where each RWAV needs to be inserted into WZSound.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt"
                        "-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; font-style:italic; text-decoration: underline;\">Create SD WZSound Patcher Instructions</span> Requirements:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Moved at least one instruction file to the right</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Created BRWSD Project</p></body></html>", None))
        self.patch_sd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Patch SD WZSound", None))
        self.load_sd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load SD WZSound Folder", None))
        self.label_description_patcher_hd.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This patches your RWAVs from your WZSound Patcher Instructions into an SD WZSound.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;"
                        " font-style:italic; text-decoration: underline;\">Patch to SD</span> Requirements:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Moved at least one instruction file to the right</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Created BRWSD Project</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Created WZSound Patcher Instructions</p></body></html>", None))
        self.patch_hd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Patch HD WZSound", None))
        self.load_hd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load HD WZSound Folder", None))
        self.label_description_patcher_sd.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This patches your RWAVs from your BRWSD Project into an HD WZSound. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; font-style:it"
                        "alic; text-decoration: underline;\">Patch to HD</span> Requirements:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Moved at least one instruction file to the right</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Created BRWSD Project</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - Have HD WZSound</p></body></html>", None))
    # retranslateUi

