import QtQuick 1.1
import "components"

Rectangle { // complete main "page"
    id: qp_main_window

    color: "lightgrey"

    property alias mail_listview: qp_mail_preview_listview
    property alias mail_text: content_text.text

    Rectangle { // mail preview list window
        id: qp_mail_preview

        width: parent.width * 0.28
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
            // Just placeholder for real one!
            footer: Rectangle {
                        height: qp_main_window.height / 10
                        width: parent.width
                        color: "lightgrey"
            }

            onMovementEnded: {
                if(atYEnd) {
                    console.log("end of list");
                    qp_mail_preview_listview.footer = loadmoreButton
                }
            }
        }

        Component {
            id: loadmoreButton

            Rectangle {
                width: parent.width
                height: qp_main_window.height / 10
                color: "lightgrey"
                border.color: "darkgrey"

                Text {
                    anchors.centerIn: parent
                    text: "+ load more"
                    color: "steelblue"
                    font.bold: true
                }

                MouseArea{
                    id: loadmoreClick
                    anchors.fill: parent

                    onClicked: {
                        console.log("load more mails!");
                        var count = qp_mail_preview_listview.count
                        mail.load_more_mails(count)
                        qp_mail_preview_listview.currentIndex = count-1
                    }
                }
            }
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

        Rectangle {
           id: mail_info_bar

           anchors.top: parent.top
           anchors.left: parent.left

           height: parent.height * 0.15
           width: parent.width

           color: "lightgrey"

           border.color: "darkgrey"

           Column {
               id: informations

               spacing: 5

               height: parent.height

               anchors.left: parent.left
               anchors.leftMargin: 40
               anchors.top: parent.top
               anchors.topMargin: 10

               Text {
                   id: mail_info_from

                   text: "<b>From</b>: "+qp_mail_preview_listview.model.get_sender(qp_mail_preview_listview.currentIndex)
                   font.pixelSize: parent.height * 0.15
               }

               Text {
                   id: mail_info_subject

                   text: "<b>Subject</b>: "+qp_mail_preview_listview.model.get_subject(qp_mail_preview_listview.currentIndex)
                   font.pixelSize: parent.height * 0.15
               }

               Text {
                   id: mail_info_date

                   text: "<b>Date</b>: "+qp_mail_preview_listview.model.get_date(qp_mail_preview_listview.currentIndex)
                   font.pixelSize: parent.height * 0.15
               }
           }
        }

        Flickable {
            id: full_content_listview

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: mail_info_bar.bottom
            anchors.topMargin: 10

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
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                onLinkActivated: console.log(link + " link activated")
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

        Button {
            id: search_button
            width:  app_window.width * 0.08
            height: app_window.height * 0.08
            buttonIcon: "img/search.png"
            onClick: {
                if (app_window.state == "show_search") { app_window.state = ""}
                else {app_window.state = "show_search"}
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
                mail.delete_mails(uid, index)
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
