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
                id: inbox_username

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Username:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                id: inbox_username_edit
                width: (parent.width - inbox_username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: inbox_username.verticalCenter
            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: inbox_password

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Password:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                id: inbox_password_edit
                width: (parent.width - inbox_username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: inbox_password.verticalCenter

                echoMode: TextInput.Password

            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: inbox_server

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "IMAP server:"
                font.pixelSize: parent.height / 4
            }

            LineEdit {
                id: inbox_server_edit
                width: (parent.width - inbox_username.width) * 0.9
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: inbox_server.verticalCenter
            }
        }

        Item {

            height: parent.height / 5
            width: parent.width

            Text {
                id: inbox_ssl

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                text: "Use SSL:"
                font.pixelSize: parent.height / 4
            }

            Switch {
                id: inbox_ssl_switch
                height: parent.height * 0.5
                anchors.right: parent.right
                anchors.verticalCenter: inbox_ssl.verticalCenter

                round: true
                onStatusChanged: {

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
            buttonIcon: "img/yes.png"

            onClick: {
                var type = "" // type is for later implementing pop/imap selection
                var user = inbox_username_edit.text
                var pass = inbox_password_edit.text
                var server = inbox_server_edit.text
                var ssl = inbox_ssl_switch.status

                mail.save_inbox_server_settings(type, user, pass, server, ssl)  // saving settings via programm logic
                mail.load_inbox_server_settings()                               // loading just a moment ago changed settings
                mail.refresh_mails()                                            // refresh mails now with latest settings
                app_window.state = ""
            }
        }

        Button {
            id: close
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/delete.png"

            onClick: {
                inbox_username_edit.text = ""
                inbox_password_edit.text = ""
                inbox_server_edit.text = ""
                inbox_ssl_switch.status = false
                app_window.state = ""
            }
        }
    }
}
