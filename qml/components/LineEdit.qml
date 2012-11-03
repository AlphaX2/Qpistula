import QtQuick 1.1

Rectangle {
    id: line

    property alias echoMode: edit.echoMode
    property alias text: edit.text

    width: parent.width - (parent.width * 0.1)
    height: parent.height / 5

    smooth: true
    radius: 10
    border.color: edit.activeFocus ? "steelblue" : "darkgrey"
    border.width: 2
    clip: true

    gradient: Gradient {
        GradientStop {position: 0.0; color: "darkgrey"}
        GradientStop {position: 0.1; color: "white"}
        GradientStop {position: 0.95; color: "white"}
        GradientStop {position: 1.0; color: "darkgrey"}

    }

    TextInput {
        id: edit
        width: parent.width * 0.9
        height: parent.height * 0.9

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter

        font.pixelSize: parent.height * 0.8
        cursorVisible: false
    }
}


