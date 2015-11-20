import QtQuick 1.0

Rectangle {
   id: window
   width: 1600
   height: 900

   property real log_stream_ratio: 0.3
   property real log_stream_margin: 10
   property real options_width: 50
   property real ui_height: 200
   property real height_M: 13 // Get text size for the given machine pixels
   property real width_M: 8
   // property real command_line_height: // fontsize + a margin
   // property real command_status_height: // command line + margin

   property color monokai_dark_grey: "#272822"
   property color monokai_light_grey: "#757575"
   property color monokai_orange: "#FD971F"
   property color cartography_dark_brown: "#662506"
   property color cartography_brown: "#993404"
   property color cartography_light_yellow: "#fff7bc"
   property color light_yellow: "#ffeda0"
   property color light_yellow_cold: "#edf8b1"
   property color light_yellow_green: "#c7e9b4"
   property color error_red: "#f03b20"

   property color log_background: monokai_dark_grey // brown "#662506" // "red" // Monokai dark grey "#272822"
   property color log_general_text: cartography_light_yellow // "black"
   // color: "#fe9929" // "#f03b20" // "#ec7014" // "#cc4c02" // Monokai orange "#FD971F"
   property color oper_background: cartography_brown
   property color message_status_color: "red"
   color: log_background

   function setColor() {
       // TODO: what is the type??
       window.color = '#7fcdbb';
   }

   signal redclick


   // ScrollView { // TODO: make the scroll to log area for reviewing DQM
    // anchors.left: options.right

      Rectangle {
      id: operation_field
      // height: 1600
      anchors {left: options.right; // parent.left;
               right: parent.right;
               bottom: parent.bottom;}

        Rectangle {
          id: ui
          // width: window.width
          height: ui_height
          border { width: 4; color: cartography_dark_brown}
          color: cartography_brown // cartography_dark_brown //
          anchors {bottom: parent.bottom;
                   left: parent.left;
                   right: parent.right}
          // radius: 5

          Rectangle {
            id: ui_comm
            width: parent.width
            height: 30
            color: "red"
            border.width: 1
            anchors {top: parent.top;
                     left: parent.left}

            Rectangle {
              id: message_status
              // width: parent.width
              height: parent.height
              border {width: 1; color: cartography_dark_brown}
              anchors {top: parent.top;
                       left: parent.left;
                       right: parent.right;
                       leftMargin: 100}
              color: message_status_color
            }

          // TODO: somehow do it text-centered way
          // the comline should enlarge to the bottom,
          // if multiline text is inputed
          Rectangle {
            id: command_line
            // visible: false
            color: "white" // "white"
            height: 24// parent.height - parent.border - 4
            width: 80 * width_M // kind of 80 characterswide?
            border {width: 1;
                    color: cartography_dark_brown}
            radius: 5
            anchors {verticalCenter: parent.verticalCenter;
                     left: parent.left;
                     leftMargin: window.width * log_stream_ratio + log_stream_margin}

            TextInput {
               id: command_input
               // anchors.fill: parent
               height: height_M
               // width: parent.width
               color: "black"
               text: "commmmmm"
               anchors {//bottom: parent.bottom;
                        //bottomMargin: 2;
                        left: parent.left
                        leftMargin: 5;
                        right: parent.right;
                        rightMargin: 5;
                        verticalCenter: parent.verticalCenter}
            }
          }
       }
      }

      Rectangle {
       id: log_stream
       // width: window.width
       // anchors {top: parent.top; bottom: ui.top}
       anchors {bottom: ui.top;
                top: parent.top
                left: parent.left;
                right: parent.right}
       color: log_background

        Text {
         id: log_comment
         width: window.width * log_stream_ratio
         color: monokai_light_grey // log_general_text
         horizontalAlignment: Text.AlignRight
         verticalAlignment: Text.AlignBottom
         anchors {left: parent.left;
                  top: parent.top;
                  bottom: parent.bottom;
                  margins: log_stream_margin}
         text: "Comment"
         MouseArea {
          anchors.fill: parent
          onEntered: {
            console.log("Mouse on the comment!")
            parent.color = cartography_light_yellow
          }
          onExited: {parent.color = monokai_light_grey;}
         }
        }

        Text {
         id: log_text
         // width: window.width * 0.38
         text: "Log Text\n" + "Window Height = " + window.height + "\nWindow Width = " + window.width
         color: log_general_text
         verticalAlignment: Text.AlignBottom
         anchors {left: log_comment.right;
                  right: parent.right
                  top: parent.top;
                  bottom: parent.bottom;
                  margins: log_stream_margin}
        }
      }
    }
  //}

   Rectangle {
    id: options
    width: options_width
    color: monokai_light_grey
    anchors {top: parent.top;
             left: parent.left;
             bottom: parent.bottom}
   }
    // MouseArea {
         // anchors.fill: parent
         // onClicked: {
             // console.log("Mouse clicked!", parent.color)
             // // if (parent.color == "#000000")
             // if (parent.color == "#f03b20")
             // {
                 // redclick();
                 // // parent.color = 'blue';
                 // parent.color = '#ffeda0';
             // }
             // else
                 // // parent.color = 'black';
                 // parent.color = '#f03b20';
         // }
    // }
}
