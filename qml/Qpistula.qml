import QtQuick 1.1
import "components"

Rectangle { // complete main "page"
    id: qp_main_window

    color: "lightgrey"

    property alias mail_listview: qp_mail_preview_listview
    property alias mail_text: content_text.text

    Rectangle { // mail preview list window
        id: qp_mail_preview

        width: parent.width * 0.25
        height: parent.height * 0.91

        anchors.top: parent.top
        anchors.left: parent.left

        color: "lightgrey"

        border.color: "darkgrey"
        border.width: 1

        ListView {
            id: qp_mail_preview_listview

            anchors.fill: qp_mail_preview

            clip: true
            model: mailListModel

            delegate: Mail_Preview_Delegator{}
        }
    }

    Rectangle { // full content window
        id: qp_mail_full_content

        width: parent.width - (qp_mail_preview.width + parent.width * 0.02)
        height: parent.height * 0.91

        anchors.top: parent.top
        anchors.left: qp_mail_preview.right
        anchors.leftMargin: (qp_main_window.width - qp_mail_preview.width - qp_mail_full_content.width) / 2

        border.color: "darkgrey"
        border.width: 1

        Flickable {
            id: full_content_listview

            anchors.centerIn: parent

            width: parent.width * 0.95
            height: parent.height * 0.95
            clip: true

            flickableDirection: Flickable.VerticalFlick

            Text {
                id: content_text

                width: parent.width * 0.99

                anchors.left: parent.left
                anchors.leftMargin: 20

                color: "black"
                text: ""
                textFormat: Text.RichText
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }
        }
    }

    Row { // refresh and new mail button
        id: refresh_new_buttons
        anchors.top: qp_mail_preview.bottom
        anchors.horizontalCenter: qp_mail_preview.horizontalCenter


        Button {
            id: refresh_mail_buttons
            width:  qp_main_window.width * 0.08
            height: qp_main_window.height * 0.08
            buttonIcon: "img/mail-refresh.png"
            onClick: {mail.refresh_mails()}
        }


        Button {
            id: new_mail_button
            width: qp_main_window.width * 0.08
            height: qp_main_window.height * 0.08
            buttonIcon: "img/document-new.png"
            onClick: {
                if (app_window.state == "write_new_mail") { app_window.state = ""}
                else {app_window.state = "write_new_mail"}
            }
        }
    }

    Row { // reply, forward, delete button
        id: mail_work_buttons

        anchors.horizontalCenter: qp_mail_full_content.horizontalCenter
        anchors.top: qp_mail_full_content.bottom

        Button {
            id: reply_mail_button
            width: qp_main_window.width * 0.08
            height: qp_main_window.height * 0.08
            buttonIcon: "img/reply.png"
        }

        Button {
            id: forward_mail_button
            width: qp_main_window.width * 0.08
            height: qp_main_window.height * 0.08
            buttonIcon: "img/forward.png"
        }

        Button {
            id: delete_mail_button
            width: qp_main_window.width * 0.08
            height: qp_main_window.height * 0.08
            buttonIcon: "img/delete.png"
        }
    }

    Button {
        id: settings
        width: qp_main_window.width * 0.08
        height: qp_main_window.height * 0.08

        anchors.right: qp_mail_full_content.right
        anchors.top: qp_mail_full_content.bottom

        buttonIcon: "img/settings.png"

        onClick: {
            app_window.state = "show_menu"
        }
    }
}
