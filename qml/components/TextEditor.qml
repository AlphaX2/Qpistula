import QtQuick 1.1


Rectangle {
    id: editor_window

    property alias editorTextSize: editor.font.pointSize
    property bool showBorder: false

    color: "white"
    border.color: showBorder == true ? "darkgrey" : "white"
    border.width: showBorder == true ? 1 : 0

    Flickable {
        id: editor_flicker

        width: parent.width
        height: parent.height
        contentWidth: editor.paintedWidth
        contentHeight: editor.paintedHeight
        clip: true

        function ensureVisible(r)
             {
                 if (contentX >= r.x)
                     contentX = r.x;
                 else if (contentX+width <= r.x+r.width)
                     contentX = r.x+r.width-width;
                 if (contentY >= r.y)
                     contentY = r.y;
                 else if (contentY+height <= r.y+r.height)
                     contentY = r.y+r.height-height;
             }

        TextEdit {
            id: editor

            width: editor_flicker.width
            height: editor_flicker.height

            font.pointSize: 12
            textFormat: TextEdit.RichText
            wrapMode: TextEdit.WordWrap
            onCursorRectangleChanged: editor_flicker.ensureVisible(cursorRectangle)
        }
    }
}
