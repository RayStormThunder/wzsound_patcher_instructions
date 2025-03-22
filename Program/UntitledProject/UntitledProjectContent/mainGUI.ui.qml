

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
    width: Constants.width
    height: Constants.height
    color: "#212121"


    Frame {
        id: frame
        x: 0
        y: 47
        width: 1920
        height: 1033

        TabBar {
            id: tabBar
            x: -18
            y: -12
            width: 1920
            height: 35
            currentIndex: -1

            TabButton {
                id: tabButton
                text: qsTr("Test 1")
            }

            TabButton {
                id: tabButton1
                text: qsTr("Test 2")
            }

            TabButton {
                id: tabButton2
                text: qsTr("Test 3")
            }
        }
    }
}

/*##^##
Designer {
    D{i:0}D{i:2;invisible:true}
}
##^##*/
