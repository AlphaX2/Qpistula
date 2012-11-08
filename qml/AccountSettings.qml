import QtQuick 1.1
import "components"

Rectangle {
    id: settings_window

    width: parent.width * 0.4
    height: parent.height * 0.8

    Component.onCompleted: {
        var conf_str = mail.get_conf_for_gui()
        var conf_list = conf_str.split(',')

        mail_name_edit.text = conf_list[1]
        inbox_username_edit.text = conf_list[2]
        inbox_password_edit.text = conf_list[3]
        inbox_server_edit.text = conf_list[4]

        if (conf_list[5] === "True") {inbox_ssl_switch.status = true}
        else {inbox_ssl_switch.status = false}

        outbox_username_edit.text = conf_list[6]
        outbox_password_edit.text = conf_list[7]
        outbox_server_edit.text = conf_list[8]

        if (conf_list[9] === "True") {outbox_ssl_switch.status = true}
        else {outbox_ssl_switch.status = false}
    }

    radius: 10

    color: "lightgrey"
    border.color: "darkgrey"
    border.width: 1

    Text {
        id: title

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 5

        text: "Account Settings"
        font.pixelSize: parent.height * 0.06
        font.bold: true
    }


    Item {

        height: parent.height / 9
        width: parent.width * 0.9

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: title.bottom

        Text {
            id: mail_name

            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            text: "Mail adress:"
            font.pixelSize: parent.height / 4
        }

        LineEdit {
            id: mail_name_edit
            width: (parent.width - inbox_username.width) * 0.9
            height: parent.height * 0.5
            anchors.right: parent.right
            anchors.verticalCenter: mail_name.verticalCenter
        }
    }

    Rectangle {
        id: tab_window

        width: parent.width
        height: parent.height * 0.7

        anchors.bottom: parent.bottom

        border.color: "darkgrey"
        border.width: 1

        color: "lightgrey"

        Rectangle {
            id: inbox_server_settings

            width: parent.width / 2
            height: parent.height * 0.1

            anchors.top: tab_window.top

            color: "lightgrey"
            border.color: "darkgrey"
            border.width: 1

            Text {
                id: inbox_tab_text
                anchors.centerIn: parent
                text: "Inbox server settings"
                color: "black"
            }

            MouseArea {
                anchors.fill: parent

                onClicked: {inbox_server_settings.color = "lightgrey"; outbox_server_settings.color = "darkgrey";
                            inbox_tab_text.color = "black"; outbox_tab_text.color = "grey"
                            outbox_elements_column.visible = false; inbox_elements_column.visible = true
                }
            }
        }

        Rectangle {
            id: outbox_server_settings

            width: parent.width / 2
            height: parent.height * 0.1

            anchors.top: tab_window.top
            anchors.left: inbox_server_settings.right

            color: "darkgrey"
            border.color: "darkgrey"
            border.width: 1

            Text {
                id: outbox_tab_text
                anchors.centerIn: parent
                text: "Outbox server settings"
                color: "grey"
            }

            MouseArea {
                anchors.fill: parent

                onClicked: {outbox_server_settings.color = "lightgrey"; inbox_server_settings.color = "darkgrey";
                            outbox_tab_text.color = "black"; inbox_tab_text.color = "grey"
                            inbox_elements_column.visible = false; outbox_elements_column.visible = true
                }
            }
        }


        Column {
            id: inbox_elements_column

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom

            height: parent.height - inbox_server_settings.height
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

        Column {
            id: outbox_elements_column

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom

            height: parent.height - inbox_server_settings.height
            width: parent.width * 0.9

            visible: false

            Item {

                height: parent.height / 5
                width: parent.width

                Text {
                    id: outbox_username

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Username:"
                    font.pixelSize: parent.height / 4
                }

                LineEdit {
                    id: outbox_username_edit
                    width: (parent.width - outbox_username.width) * 0.9
                    height: parent.height * 0.5
                    anchors.right: parent.right
                    anchors.verticalCenter: outbox_username.verticalCenter
                }
            }

            Item {

                height: parent.height / 5
                width: parent.width

                Text {
                    id: outbox_password

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Password:"
                    font.pixelSize: parent.height / 4
                }

                LineEdit {
                    id: outbox_password_edit
                    width: (parent.width - outbox_username.width) * 0.9
                    height: parent.height * 0.5
                    anchors.right: parent.right
                    anchors.verticalCenter: outbox_password.verticalCenter

                    echoMode: TextInput.Password

                }
            }

            Item {

                height: parent.height / 5
                width: parent.width

                Text {
                    id: outbox_server

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "SMTP server:"
                    font.pixelSize: parent.height / 4
                }

                LineEdit {
                    id: outbox_server_edit
                    width: (parent.width - outbox_username.width) * 0.9
                    height: parent.height * 0.5
                    anchors.right: parent.right
                    anchors.verticalCenter: outbox_server.verticalCenter
                }
            }

            Item {

                height: parent.height / 5
                width: parent.width

                Text {
                    id: outbox_ssl

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Use SSL:"
                    font.pixelSize: parent.height / 4
                }

                Switch {
                    id: outbox_ssl_switch
                    height: parent.height * 0.5
                    anchors.right: parent.right
                    anchors.verticalCenter: outbox_ssl.verticalCenter

                    round: true
                    onStatusChanged: {

                    }
                }
            }
        }
    }

    Row {
        id: yes_no_button_row
        height: children.height
        width: children.width
        anchors.horizontalCenter: settings_window.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10

        Button {
            id: okay
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/yes.png"

            onClick: {
                var type = "imap" // type is for later implementing pop/imap selection
                var mailname = mail_name_edit.text // mail should hold mail adress

                var in_user = inbox_username_edit.text
                var in_pass = inbox_password_edit.text
                var in_server = inbox_server_edit.text
                var in_ssl = inbox_ssl_switch.status

                var out_user = outbox_username_edit.text
                var out_pass = outbox_password_edit.text
                var out_server = outbox_server_edit.text
                var out_ssl = outbox_ssl_switch.status

                // saving settings via programm logic
                mail.save_server_settings(type,
                                          mailname,

                                          in_user,
                                          in_pass,
                                          in_server,
                                          in_ssl,

                                          out_user,
                                          out_pass,
                                          out_server,
                                          out_ssl)

                // loading just a moment ago changed settings
                mail.load_server_settings()

                // refresh mails now with latest settings
                mail.refresh_mails()

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

                outbox_username_edit.text = ""
                outbox_password_edit.text = ""
                outbox_server_edit.text = ""
                outbox_ssl_switch.status = false

                app_window.state = ""
            }
        }
    }
}
