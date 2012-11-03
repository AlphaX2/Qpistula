import QtQuick 1.1

Rectangle {
    id: scrollbar

    property Flickable flickArea

    width: parent.width
    height: flickArea.visibleArea.heightRatio * flickArea.height

    y: flickArea.visibleArea.yPosition * flickArea.height
    color: "lightgrey"
    opacity: flickArea.moving ? 0.6 : 0.0
}

