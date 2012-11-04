import QtQuick 1.1
import "components"

Rectangle {
    id: app_window

    // it's scaleable via programm logic
    width: 1280
    height: 720

    Qpistula {
        id: main_window
        width: parent.width
        height: parent.height
    }


    WriteMail {
        id: write_window
        y: -height // parent.y - parent.height
        visible: false
    }

    DefaultMenu {
        id: menu
        opacity: 0
    }

    AccountSettings {
        id: acc_settings

        anchors.horizontalCenter: parent.horizontalCenter
        y: -height

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
        },

        State {
            name: "show_acc_settings"
            PropertyChanges {target: acc_settings; opacity: 1.0; y: 0 }
        }
    ]

    transitions: [
        Transition {
            from: ""
            to: "write_new_mail"
            PropertyAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
        },

        Transition {
            from: "write_new_mail"
            to: ""
            PropertyAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
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
        },

        Transition {
            from: ""
            to: "show_acc_settings"
            PropertyAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
            PropertyAnimation { properties: "opacity"; duration: 250}
        },

        Transition {
            from: "show_acc_settings"
            to: ""
            PropertyAnimation { properties: "y"; easing.type: Easing.InOutQuad; duration: 500}
            PropertyAnimation { properties: "opacity"; duration: 2000}
        }
    ]
}

