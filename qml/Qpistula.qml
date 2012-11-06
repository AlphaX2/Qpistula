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

        Scrollbar {
            id: scrollbar_list

            anchors.left: qp_mail_preview_listview.left
            anchors.leftMargin: 5
            width: 3
            flickArea: qp_mail_preview_listview
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
            contentHeight: content_text.height
            contentWidth: content_text.width
            clip: true

            flickableDirection: Flickable.VerticalFlick

            Text {
                id: content_text

                width: qp_mail_full_content.width * 0.95

                anchors.left: parent.left
                anchors.leftMargin: 20

                color: "black"
                text: qp_mail_preview_listview.model.get_message(qp_mail_preview_listview.currentIndex)
                font.pixelSize: full_content_listview.height / 40
                textFormat: Text.RichText
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }
        }

        Scrollbar {
            id: scrollbar

            anchors.left: full_content_listview.right
            width: 3
            flickArea: full_content_listview
        }
    }

    Row { // refresh and new mail button
        id: refresh_new_buttons
        anchors.top: qp_mail_preview.bottom
        anchors.horizontalCenter: qp_mail_preview.horizontalCenter


        Button {
            id: refresh_mail_buttons
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/mail-refresh.png"
            onClick: {mail.refresh_mails()}
        }


        Button {
            id: new_mail_button
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
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
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/reply.png"

            onClick: {
                var index = qp_mail_preview_listview.currentIndex
                var model = qp_mail_preview_listview.model

                app_window.state = "write_new_mail"

                var sender = model.get_sender(index)
                var subject = model.get_subject(index)
                var content = model.get_message(index)
                var date = model.get_date(index)

                write_window.to = sender
                write_window.subject = "Re: "+subject
                write_window.content = "<br><br><br>---------------------------------<br>"+date+"<br><br>"+content
            }
        }

        Button {
            id: forward_mail_button
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/forward.png"

            onClick: {
                var index = qp_mail_preview_listview.currentIndex
                var model = qp_mail_preview_listview.model

                app_window.state = "write_new_mail"

                var subject = model.get_subject(index)
                var content = model.get_message(index)
                var date = model.get_date(index)

                write_window.subject = "Fwd: "+subject
                write_window.content = "<br><br><br>---------------------------------<br>"+date+"<br><br>"+content
            }
        }

        Button {
            id: delete_mail_button
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/delete.png"

            onClick: {
                var index = qp_mail_preview_listview.currentIndex
                var model = qp_mail_preview_listview.model
                var uid = model.get_uid(index)
                console.log(uid)
                mail.delete_mails(uid)
            }
        }
    }

    Button {
        id: settings
        width:  app_window.width * 0.08
        height: app_window.height * 0.08

        anchors.right: qp_mail_full_content.right
        anchors.top: qp_mail_full_content.bottom

        buttonIcon: "img/settings.png"

        onClick: {
            app_window.state = "show_menu"
        }
    }
}
