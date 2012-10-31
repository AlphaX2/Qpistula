import QtQuick 1.1

Rectangle {
    id: mail_button

    property alias buttonWidth: mail_button.width
    property alias buttonHeight: mail_button.height
    property alias buttonIcon: button_img.source
    property alias buttonText: button_text.text

    signal click

    width: 120
    height: 60
    color: mouse.pressed ? "lightgrey" : "darkgrey"
    border.width: 1
    border.color: "white"

    MouseArea {
        id: mouse

        anchors.fill: parent

        onClicked: {
            click()
        }
    }

    Image {
        id: button_img

        anchors.centerIn: parent
        width: mail_button.width * 0.5
        height: mail_button.width * 0.5
        source: ""
        smooth: true
        }

    Text {
        id: button_text

        anchors.centerIn: parent
        text: ""
        style: Text.Outline
        styleColor: "lightgrey"
        font.bold: true
        font.pixelSize: mail_button.height * 0.5
        color: "black"
        smooth: true
        opacity: 0.65

    }
}
