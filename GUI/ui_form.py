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
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

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

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontal_1_project_buttons.addWidget(self.pushButton)


        self.vertical_main.addLayout(self.horizontal_1_project_buttons)

        self.horizontal_2_main_content = QHBoxLayout()
        self.horizontal_2_main_content.setObjectName(u"horizontal_2_main_content")
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
        self.text_description_pick = QTextEdit(self.frame_pick)
        self.text_description_pick.setObjectName(u"text_description_pick")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.text_description_pick.sizePolicy().hasHeightForWidth())
        self.text_description_pick.setSizePolicy(sizePolicy2)
        self.text_description_pick.setMinimumSize(QSize(0, 100))
        self.text_description_pick.setMaximumSize(QSize(16777215, 140))
        self.text_description_pick.setReadOnly(True)

        self.vertical_description.addWidget(self.text_description_pick)


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

        self.text_description_edit = QTextEdit(self.frame_edit)
        self.text_description_edit.setObjectName(u"text_description_edit")
        self.text_description_edit.setMinimumSize(QSize(0, 100))
        self.text_description_edit.setMaximumSize(QSize(16777215, 140))
        self.text_description_edit.setReadOnly(True)

        self.verticalLayout_12.addWidget(self.text_description_edit)


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
        self.button_create_brwsd = QPushButton(self.frame_1_create_brwsd)
        self.button_create_brwsd.setObjectName(u"button_create_brwsd")

        self.verticalLayout_2.addWidget(self.button_create_brwsd)

        self.label_description_brwsd = QLabel(self.frame_1_create_brwsd)
        self.label_description_brwsd.setObjectName(u"label_description_brwsd")
        self.label_description_brwsd.setFrameShape(QFrame.Shape.NoFrame)
        self.label_description_brwsd.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_description_brwsd.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_description_brwsd)


        self.vertical_create.addWidget(self.frame_1_create_brwsd)

        self.frame_2_create_wzsound = QFrame(self.centralwidget)
        self.frame_2_create_wzsound.setObjectName(u"frame_2_create_wzsound")
        self.frame_2_create_wzsound.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2_create_wzsound.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2_create_wzsound)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.button_create_wzsound = QPushButton(self.frame_2_create_wzsound)
        self.button_create_wzsound.setObjectName(u"button_create_wzsound")

        self.verticalLayout_3.addWidget(self.button_create_wzsound)

        self.label_description_wzsound = QLabel(self.frame_2_create_wzsound)
        self.label_description_wzsound.setObjectName(u"label_description_wzsound")
        self.label_description_wzsound.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_description_wzsound.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_description_wzsound)


        self.vertical_create.addWidget(self.frame_2_create_wzsound)


        self.horizontal_2_main_content.addLayout(self.vertical_create)

        self.horizontal_2_main_content.setStretch(0, 3)
        self.horizontal_2_main_content.setStretch(1, 1)

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
        self.button_create_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Project", None))
        self.button_load_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Load Project", None))
        self.button_convert_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Convert Project", None))
        self.pushButton.setText(QCoreApplication.translate("WZSPI_MainWindow", u"PushButton", None))
        self.button_create_instructions.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Instructions", None))
        self.button_edit_instructions.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Edit Instructions", None))
        self.label_options.setText(QCoreApplication.translate("WZSPI_MainWindow", u"All Options", None))
        self.button_move.setText(QCoreApplication.translate("WZSPI_MainWindow", u"<-Move->", None))
        self.label_project.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Your Project", None))
        self.text_description_pick.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This section controls what RWAV files you want to edit in your project. You will see a list of groups of sound effects in &quot;All Options.&quot; Those are a collection of sound effects to extract. You can select the ones you want and click &quot;&lt;-Move-&gt;&quot; to move it to &quot;Your Project.&quot; Once you have selected all the RWAV files you want to extract. Move to the &quot;Create Project"
                        " BRWSD&quot; step.<br /><br />If you want to extract sound effects that aren't specified by &quot;All Options&quot; you can Create or Edit your own instructions by hitting the appropiate button.</p></body></html>", None))
        self.button_save_changes.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Save Changes", None))
        self.button_cancel_changes.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Cancel Changes", None))
        self.text_description_edit.setHtml(QCoreApplication.translate("WZSPI_MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Above is a YAML file. You can define what RWAV files you want to extract when this YAML is selected. If you go into the &quot;Indexes&quot; folder. You will see a bunch of BRWSD files. These are a collection of RWAV files. You extract a specific RWAV by stating the BRWSD you want to pull from and the Audio number.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-l"
                        "eft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Go to the 2nd tab of the following spreadsheet for documentation of indexes:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">https://docs.google.com/spreadsheets/d/1DCLMLXRMok6Iyk0BDTjtdBkzT1k1zQvzSfZXEwR0kiE/edit?gid=1359457321#gid=1359457321</p></body></html>", None))
        self.button_create_brwsd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create Project BRWSD", None))
        self.label_description_brwsd.setText(QCoreApplication.translate("WZSPI_MainWindow", u"After setting up your instructions. You can click the \"Create Project BRWSD\" button. This will extract every RWAV that the instructions specified and combine them into a single BRWSD file. You can then open this file with Brawlcrate. Every RWAV you want to edit will be there. You can make changes in that file and save your changes. Once you have edited all sound effects you want to edit. Move to the \"Create WZSound Patcher Instructions\" step.", None))
        self.button_create_wzsound.setText(QCoreApplication.translate("WZSPI_MainWindow", u"Create WZSound Patcher Instructions", None))
        self.label_description_wzsound.setText(QCoreApplication.translate("WZSPI_MainWindow", u"After you have edited every RWAV file you want. You can click the \"Create WZSound Patcher Instructions\" button. This will take the data from your project and make a folder called \"WZedit\" inside of \"Releases/{Project_Name}.\" It will contain all of your RWAV files and an instruction file that will tell SSRando how to edit the WZSound with the RWAV files provided.", None))
    # retranslateUi

