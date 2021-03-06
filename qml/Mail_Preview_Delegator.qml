import QtQuick 1.1

Component {

    Rectangle {
        id: short_mail_preview

        width: qp_mail_preview.width
        height: mail_preview_column.height

        color: ListView.isCurrentItem ? "lightgrey" : "white"
        clip: true

        Rectangle {
            id: unseen_indicator

            height: parent.height * 0.8
            width: 4

            anchors.left: mail_preview_column.left
            anchors.verticalCenter: mail_preview_column.verticalCenter
            anchors.leftMargin: 10

            color: "steelblue"
            visible: mails.unseen
        }

        Column {
            id: mail_preview_column
            spacing: 5

            width: parent.width * 0.95

            Text {
                id: from_text

                width: parent.width

                anchors.left: parent.left
                anchors.leftMargin: 20

                text: mails.sender
                color: "black"
                font.pointSize: 10
                font.bold: true

                wrapMode: Text.Wrap
                maximumLineCount: 2
            }

            Text {
                id: subject_text

                width: parent.width * 0.95

                anchors.left: parent.left
                anchors.leftMargin: 20

                text: mails.subject
                color: "black"
                font.pointSize: 10

                textFormat: Text.RichText
                wrapMode: Text.Wrap
                maximumLineCount: 2
            }

            Text {
                id: preview_text

                width: parent.width * 0.95

                anchors.left: parent.left
                anchors.leftMargin: 20

                text: mails.preview
                color: "darkgrey"
                font.pointSize: 10

                textFormat: Text.RichText
                wrapMode: Text.Wrap
                maximumLineCount: 2
            }

            Text {
                id: time_stemp

                width: parent.width * 0.95

                anchors.left: parent.left
                anchors.leftMargin: 20

                text: mails.date
                color: "steelblue"
                font.pointSize: 8
            }

            // just to have some kind of seperator between the mails
            Rectangle {
                id: bottom_spacer
                width: short_mail_preview.width * 0.9
                anchors.horizontalCenter: parent.horizontalCenter
                height: 2
                color: "lightgrey"
            }
        }


        MouseArea {
             id: open_mail_mouse_area

             anchors.fill: parent

             onClicked: {
                 mail_listview.currentIndex = index
             }
        }
    }
}
