import QtQuick 1.0

Rectangle {
   id: window
   width: 200
   height: 200
   color: "red"

   function setColor() {
       // TODO: what is the type??
       window.color = '#7fcdbb';
   }

   signal redclick

   Text {
    text: "Hello World"
    anchors.centerIn: parent
   }

   MouseArea {
        anchors.fill: parent
        onClicked: {
            console.log("Mouse clicked!", parent.color)
            // if (parent.color == "#000000")
            if (parent.color == "#f03b20")
            {
                redclick();
                // parent.color = 'blue';
                parent.color = '#ffeda0';
            }
            else
                // parent.color = 'black';
                parent.color = '#f03b20';
        }
   }
}
