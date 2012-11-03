import QtQuick 1.1

Rectangle {
    id: dialog

    width: parent.widht
    height: parent.height

    signal closed()

    property bool show_buttons

    property alias title: title.text
    property alias content: content.text

    color: "black"
    opacity: 0.9

    Rectangle {
        id: dialog_window

        width: parent.width * 0.4
        height: parent.height * 0.4

        anchors.centerIn: parent

        radius: 10
        smooth: true
        color: "transparent"

        Text {
            id: title

            anchors.top: parent.top
            anchors.left: parent.left

            text: "Information"
            color: "white"
            font.pixelSize: dialog.height * 0.05
        }

        Rectangle {
            id: deco_spacer

            width: parent.width - (title.width + deco_spacer.anchors.leftMargin)
            height: 1

            color: "#dcdcdc"

            anchors.left: title.right
            anchors.leftMargin: 10
            anchors.verticalCenter: title.verticalCenter
        }

        Rectangle {
            id: close_button

            width: dialog.height * 0.05
            height: dialog.height * 0.05

            anchors.left: deco_spacer.right
            anchors.leftMargin: 5

            radius: dialog.height

            color: "transparent"

            border.color: "#dcdcdc"
            border.width: 2

            smooth: true

            MouseArea {
                anchors.fill: parent
                onClicked: {closed()}
                }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                color: "#dcdcdc"
                text: "X"
                font.pixelSize: parent.height * 0.9
            }
        }

        Flickable {
            id: content_flick

            width: parent.width
            height: parent.height

            anchors.top: title.bottom
            anchors.topMargin: 10

            contentHeight: content.height
            contentWidth: content.width

            flickableDirection: Flickable.VerticalFlick

            clip: true

            Text {
                id: content

                width: dialog_window.width
                font.pixelSize: dialog.height * 0.03
                color: "#dcdcdc"
                wrapMode: Text.WordWrap

                horizontalAlignment: Text.AlignHCenter

                text: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat."

            }
        }

        Scrollbar {
            id: scrollbar

            anchors.left: content_flick.right

            width: 1
            flickArea: content_flick
        }
    }
}
