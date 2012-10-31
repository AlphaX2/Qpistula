import QtQuick 1.1
import "components"

Rectangle {
    id: settings_window

    width: parent.width * 0.4
    height: parent.height * 0.6

    radius: 10

    color: "lightgrey"
    border.color: "darkgrey"
    border.width: 1

    Text {
        id: title

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20

        text: "Account Settings"
        font.pixelSize: parent.height * 0.08
        font.bold: true
    }

    Column {
        id: elements_column

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: title.bottom
        anchors.topMargin: 20

        height: parent.height * 0.8
        width: parent.width * 0.9


        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: username

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Username:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                width: (parent.width - username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: username.verticalCenter
            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: password

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Password:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                width: (parent.width - username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: password.verticalCenter

                echoMode: TextInput.Password

            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: server

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "IMAP server:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                width: (parent.width - username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: server.verticalCenter
            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: ssl

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Use SSL:"
                font.pixelSize: parent.height / 4
            }

            Switch {
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: ssl.verticalCenter

                round: true
                onStatusChanged: {
                    console.log("haha haha haha")
                }
            }
        }
    }

    Row {
        height: children.height
        width: children.width
        anchors.horizontalCenter: settings_window.horizontalCenter
        anchors.bottom: settings_window.bottom

        Button {
            id: okay
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/gtk-yes.png"

            onClick: {
                app_window.state = ""
            }
        }

        Button {
            id: close
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/delete.png"

            onClick: {
                app_window.state = ""
            }
        }
    }
}
