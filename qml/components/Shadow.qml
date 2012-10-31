import QtQuick 1.1

Rectangle {
     id: container
     property string gradientType: "TopToBottom"
     property Gradient gradient
     color: "gray" // for debugging later change to Item w/o color

     Rectangle {
         id: rect
         gradient: container.gradient

         states: [
             State {
                 name: "TopToBottom"
                 when: container.gradientType == "TopToBottom"
                 PropertyChanges {
                     target: rect
                     rotation: 0
                     x: 0
                     y: 0
                     width: container.width
                     height: container.height
                 }
             },
             State {
                 name: "LeftToRight"
                 when: container.gradientType == "LeftToRight"
                 PropertyChanges {
                     target: rect
                     rotation: 270
                     transformOrigin: Item.Top
                     x: - container.height / 2
                     y: container.height / 2
                     width: container.height
                     height: container.width
                 }
             }
         ]
     }
}
