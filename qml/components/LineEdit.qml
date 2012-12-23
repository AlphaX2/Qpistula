import QtQuick 1.1

Rectangle {
    id: line

    property alias echoMode: edit.echoMode
    property alias text: edit.text
    property alias icon: icon.source

    width: parent.width * 0.9
    height: 60 //parent.height / 5

    smooth: true
    radius: 3
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
        width: (parent.width * 0.95) + icon.width
        height: parent.height * 0.9

        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        font.pixelSize: parent.height * 0.8
        cursorVisible: false

        Image {
            id: icon
            width: line.height * 0.6
            height: line.height * 0.6

            anchors.verticalCenter: edit.verticalCenter
            anchors.left: edit.right

            source: ""
        }
    }
}


