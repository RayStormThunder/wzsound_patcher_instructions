

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject

Rectangle {
    id: rectangle
    width: 1920 // Default width
    height: 1080 // Default height
    // Makes it scale with window if parent exists
    color: "#1d1d1d"
    border.color: "#303030"

    Column {
        id: column
        anchors.fill: parent

        Row {
            id: row
            y: -42
            width: 1920
            height: 42

            Button {
                id: button
                width: 960
                text: qsTr("Load Project")
                anchors.left: parent.left
                anchors.leftMargin: 0
            }

            Button {
                id: button1
                x: 960
                width: 960
                text: qsTr("Re-extract WZSound")
            }
        }

        Row {
            id: row1
            y: 0
            width: 1920
            height: 42

            Column {
                id: column1
                width: 1280
                height: 1080
            }

            Column {
                id: column3
                x: 1280
                width: 640
                height: 1080

                Column {
                    id: column4
                    width: 640
                    height: 540

                    Button {
                        id: button2
                        width: 640
                        text: qsTr("Create Project BRWSD")
                    }

                    Frame {
                        id: frame
                        width: 640
                        height: 500

                        Text {
                            id: text1
                            x: -12
                            y: -12
                            width: 640
                            height: 500
                            color: "#ffffff"
                            text: qsTr("After setting up your instructions. You can click the \"Create Project BRWSD\" button. This will extract every RWAV that the instructions specified and put combine them into a single BRWSD file. You can then open this file with Brawlcrate. Every RWAV you want to edit will be there. You can make changes in that file and save your changes.")
                            font.pixelSize: 24
                            wrapMode: Text.WordWrap
                            fontSizeMode: Text.Fit
                        }
                    }
                }

                Column {
                    id: column5
                    width: 640
                    height: 540

                    Button {
                        id: button3
                        width: 640
                        text: qsTr("Create Final Project")
                    }

                    TextArea {
                        id: textArea1
                        width: 640
                        height: 500
                        placeholderText: qsTr("Text Area")
                    }
                }
            }
        }
    }
}
