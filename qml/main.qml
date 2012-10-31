import QtQuick 1.1
import "components"

Rectangle {
    id: app_window

    Component.onCompleted: {first_msg_timer.start()}

    width: 1280
    height: 720

    /*
     there is a python function which asks for the first message text,
     due to the time difference between showing the QML window and
     fetching mails from server, this timer repeats as long as the mails
     text is empty the function to set the text and stops itself when done
    */

    Timer {
        id: first_msg_timer
        interval: 100; running: false; repeat: true
        onTriggered: {
            if(main_window.mail_text == "") {main_window.mail_text = mail.show_first_message()}
            else {first_msg_timer.stop()}
        }
    }


    Qpistula {
        id: main_window
        width: parent.width
        height: parent.height
    }


    WriteMail {
        id: write_window
        y: parent.y - parent.height
        visible: false
    }


    DefaultMenu {
        id: menu
        opacity: 0
    }


    states: [
        State {
            name: "write_new_mail"
            PropertyChanges {target: write_window; visible: true; y: 0 }
            PropertyChanges {target: main_window; visible: false; y: parent.y - parent.height}
        },

        State {
            name: "show_menu"
            PropertyChanges {target: menu; opacity: 0.9}
        }

    ]


    transitions: [
        Transition {
            from: ""
            to: "write_new_mail"
            NumberAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
        },

        Transition {
            from: "write_new_mail"
            to: ""
            NumberAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
        },

        Transition {
            from: ""
            to: "show_menu"
            NumberAnimation { properties: "opacity"; duration: 250}
        },

        Transition {
            from: "show_menu"
            to: ""
            NumberAnimation { properties: "opacity"; duration: 250}
        }
    ]
}

