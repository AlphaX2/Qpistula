import QtQuick 1.1
import "components"

Rectangle {
    id: main_editor_window

    width: parent.width
    height: parent.height * 0.6
    color: "lightgrey"

    property bool details_status: false

    property alias to: to_input.text
    property alias subject: subject.text
    property alias content: mail_editor.text

    Rectangle { //adress_data_window
        id: adress_data_window

        width: parent.width * 0.28
        height: parent.height

        color: "lightgrey"

        border.color: "darkgrey"
        border.width: 1

        Flickable {
            id: adress_data_flicker

            //anchors.fill: parent
            width: parent.width
            height: parent.height

            anchors.centerIn: parent

            flickableDirection: Flickable.VerticalFlick
            interactive: details_status

            Column {
                id: input_lines_column
                anchors.fill: parent
                spacing: 10

                Mail_LineEdit {
                    id: to_input

                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    descriptionText: "To:"
                }

                Mail_LineEdit {
                    id: bb_input

                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    descriptionText: "BB:"
                    visible: details_status
                }

                Mail_LineEdit {
                    id: cc_input

                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    descriptionText: "CC:"
                    visible: details_status
                }

                Mail_LineEdit {
                    id: subject

                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    descriptionText: "Subject:"
                }

                Button {
                    id: attachment_send_mail

                    width:  main_window.width * 0.08
                    height: main_window.height * 0.08

                    anchors.horizontalCenter: parent.horizontalCenter

                    buttonIcon: "img/mail-attachment.png"
                    visible: details_status

                    onClick: {}
                }

                Rectangle {
                    id: more_details_button

                    width: 30
                    height: 30

                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: subject.bottom
                    anchors.topMargin: 80

                    Image {
                        id: more_details_icon
                        source: "img/add.png"
                        width: parent.width
                        height: parent.height
                    }

                    MouseArea {
                        id: show_more_details

                        anchors.fill: parent
                        onClicked: {
                            if (details_status) {details_status = false}
                                else {details_status = true}
                        }
                    }
                }
            }
        }
    }

    Rectangle { //mail_editor_window
        id: mail_editor_window

        height: parent.height
        width: parent.width - adress_data_window.width

        color: "lightgrey"

        border.color: "darkgrey"
        border.width: 1

        anchors.left: adress_data_window.right
        //anchors.leftMargin: 5 //adress_data_shadow.width

        Rectangle {
            id: editor_background

            anchors.centerIn: parent

            width: parent.width * 0.98
            height: parent.height
            color: "white"
        }

       TextEditor {
            id: mail_editor

            width: parent.width * 0.9
            height: parent.height * 0.9

            showBorder: true
            anchors.centerIn: parent
       }
    }

    Row {
        anchors.horizontalCenter: adress_data_window.horizontalCenter
        anchors.bottom: adress_data_window.bottom

        spacing: 10

        Button {
            id: send_mail
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/document-send.png"
            onClick: {
                var dest = to_input.text
                var sub = subject.text
                var cont = mail_editor.text

                mail.send_mail(dest, sub, cont)
                app_window.state = ""
            }
        }

        Button {
            id: cancel_send_mail
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/delete.png"
            onClick: {
                to_input.text = ""
                subject.text = ""
                mail_editor.text = ""
                app_window.state = ""
            }
        }
    }
}
