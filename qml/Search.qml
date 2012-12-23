import QtQuick 1.1
import "components"

Rectangle {
    id: search_window

    width: 1280 //parent.width
    height: 720 //parent.height

    color: "lightgrey"

    Rectangle {
        id: search_options

        width: parent.width * 0.28
        height: parent.height * 0.91

        border.color: "darkgrey"

        Text {
            id: search_line_title

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin: 20
            anchors.leftMargin: 10

            text: "Search:"
            font.bold: true
            font.pixelSize: parent.height * 0.03
        }

        LineEdit {
            id: search_line

            anchors.top: search_line_title.bottom
            anchors.left: parent.left
            anchors.topMargin: 10
            anchors.leftMargin: 10

            height: parent.height / 20
        }

        Button {
            id: back
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.bottom

            width:  app_window.width * 0.08
            height: app_window.height * 0.08

            buttonIcon: "img/delete.png"
            onClick: {app_window.state = ""}
        }
    }
}
