import QtQuick 1.1

Rectangle {
    id: mail_button

    property alias buttonWidth: mail_button.width
    property alias buttonHeight: mail_button.height
    property alias buttonIcon: button_img.source

    signal click

    width: 120
    height: 60
    color: mouse.pressed ? "lightgrey" : "white"

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
        width: mail_button.width * 0.3
        height: mail_button.width * 0.3
        source: ""
        }
}
