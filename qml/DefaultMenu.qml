import QtQuick 1.1
import "components"

Rectangle {
   id: background

   property alias button1Text: menu1.buttonText
   property alias button2Text: menu2.buttonText
   property alias button3Text: menu3.buttonText
   property alias button4Text: menu4.buttonText

   width: parent.width
   height: parent.height

   color: "black"

   MouseArea {
       anchors.fill: parent
       onClicked: {
           app_window.state = ""
       }
   }

       Column {
            id: menu_buttons

            width: parent.width * 0.4
            height: parent.height * 0.4
            anchors.centerIn: parent

                Button {
                    id: menu1

                    width: parent.width
                    height: parent.height * 0.15
                    buttonText: "Add account"
                }

                Button {
                    id: menu2

                    width: parent.width
                    height: parent.height * 0.15
                    buttonText: "Account settings"

                    onClick: {
                        app_window.state = ""
                        app_window.state = "show_acc_settings"
                    }
                }

                Button {
                    id: menu3

                    width: parent.width
                    height: parent.height * 0.15
                    buttonText: "General settings"
                }

                Button {
                    id: menu4

                    width: parent.width
                    height: parent.height * 0.15
                    buttonText: "Logout"
                }
            }
       }
