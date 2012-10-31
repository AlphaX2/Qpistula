import QtQuick 1.1

Rectangle {
    id: line
    width: parent.width * 0.9
    height: parent.height / 8
    color: "transparent"
    clip: true

    property alias text: input_text.text
    property alias bold: input_text.font.bold

    Text {
        id: input_text

        text: ""
        font.pixelSize: parent.height * 0.5
        font.bold: true
    }

    TextInput {
        id: edit

        width: line.width - input_text.width

        anchors.left: input_text.right
        anchors.leftMargin: 20

        font.pixelSize: parent.height * 0.5
        cursorVisible: false
    }

    Rectangle {
        id: input_underline

        width: edit.width
        height: 1

        anchors.left: edit.left
        anchors.bottom: edit.bottom

        color: "steelblue"

    }
}


