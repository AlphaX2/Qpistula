import QtQuick 1.1

Rectangle {
    id: main

    signal statusChanged

    property bool status: false
    property bool round: false

    property Gradient switch_off: Gradient {
        GradientStop {position: 0.0; color: "#dcdcdc"}
        GradientStop {position: 1.0; color: "lightgrey"}
    }

    property Gradient switch_on: Gradient {
        GradientStop {position: 0.0; color: "steelblue"}
        GradientStop {position: 0.5; color: "darkblue"}
        GradientStop {position: 1.0; color: "steelblue"}
    }

    width: 150
    height: width/2

    smooth: true
    border.color: "darkgrey"
    border.width: 2
    radius: round == true ? parent.height/2 : 5

    gradient: main.status == true ? switch_on : switch_off

    Text {
        id: on_text

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: parent.width * 0.2

        smooth: true
        text: "ON"
        font.bold: true
        font.pixelSize: parent.height * 0.4
        color: "white"
        opacity: status == true ? 1.0 : 0.0
    }

    Text {
        id: off_text

        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.rightMargin: parent.width * 0.2

        smooth: true
        text: "OFF"
        font.bold: true
        font.pixelSize: parent.height * 0.4
        color: "black"
        opacity: status == false ? 1.0 : 0.0
    }

    MouseArea {
        id: switch_flick

        anchors.fill: parent
        clip: true

        drag.target: switch_button
        drag.axis: Drag.XAxis
        drag.minimumX: 0
        drag.maximumX: main.width - switch_button.width

        onReleased: {
            if (mouseX > 50) {status = true}
            if (mouseX < 50) {status = false}

            // emits signal
            statusChanged()
        }
    }

    Rectangle {
        id: switch_button

        width: parent.height * 0.94
        height: parent.height * 0.94

        anchors.verticalCenter: main.verticalCenter
        x: status == false ? 0 : switch_flick.drag.maximumX
        smooth: true
        radius: round == true ? parent.height/2 : 5
        border.color: "grey"
        gradient: Gradient {
            GradientStop {position: 0.0; color: "#dcdcdc"}
            GradientStop {position: 1.0; color: "white"}
        }
    }
}
