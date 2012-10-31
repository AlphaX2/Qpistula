import QtQuick 1.1

Rectangle {
    id: line
    width: parent.width - (parent.width * 0.1)
    height: parent.height / 5
    color: "white"
    radius: 10
    border.color: edit.activeFocus ? "steelblue" : "white"
    border.width: 2
    clip: true

    TextInput {
        id: edit
        width: parent.width * 0.9
        height: parent.height * 0.9

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter

        font.pointSize: 16
        cursorVisible: false
    }
}


