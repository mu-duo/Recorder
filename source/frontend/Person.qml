pragma ComponentBehavior: Bound
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Item {
    id: person

    // 数据模型
    ListModel {
        id: personRecord
    }

    Rectangle {
        id: backgroundRect

        anchors.fill: parent
        color: "#f4f4f4ff"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 10

            // 任务列表
            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 5
                smooth: true

                model: personRecord

                delegate: Rectangle {
                    id: recordItem

                    required property int index
                    required property string text
                    required property var birthday

                    property int dayCountText: {
                        var today = new Date();
                        var timeDiff = today - birthday;
                        return Math.floor(timeDiff / (1000 * 60 * 60 * 24));
                    }

                    width: ListView.view.width
                    height: 50
                    color: exitColor
                    radius: 10

                    property color enterColor: "#fcfcfc"
                    property color exitColor: backgroundRect.color

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true

                        onEntered: parent.color = parent.enterColor
                        onExited: parent.color = parent.exitColor

                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        onClicked: mouse => {
                            if (mouse.button === Qt.RightButton) {
                                contextMenu.popup();
                            }
                        }
                    }

                    Menu {
                        id: contextMenu

                        width: 180

                        // 菜单样式
                        background: Rectangle {
                            color: "#fcfcfcff"
                            radius: 6
                            border.color: "#ecececff"
                            border.width: 1
                        }

                        MenuItem {
                            text: "删除任务"
                            onTriggered: {
                                person.removeRecord(recordItem.index);
                            }
                        }
                        MenuItem {
                            text: "重置计时"
                            onTriggered: {
                                recordItem.reset();
                            }
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.RightButton
                        onClicked: mouse => {
                            if (mouse.button === Qt.RightButton) {
                                contextMenu.popup();
                            }
                        }
                    }

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 10

                        Text {
                            id: contentText
                            Layout.fillWidth: true
                            text: recordItem.text
                            font.pixelSize: 16
                        }

                        Text {
                            id: dayCountText
                            text: recordItem.dayCountText + " 天"
                            font.pixelSize: 14
                            color: "#666666"
                        }
                    }

                    function reset() {
                        birthday = new Date();
                    }
                }
            }

            // 输入区域
            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                spacing: 10

                TextField {
                    id: inputField
                    // size
                    implicitHeight: parent.height
                    Layout.fillWidth: true
                    leftPadding: 20

                    placeholderText: "添加新任务..."
                    font.pixelSize: 16
                    verticalAlignment: TextInput.AlignVCenter
                    horizontalAlignment: TextInput.AlignLeft

                    background: Rectangle {
                        radius: 10
                        border.color: inputField.activeFocus ? "#b1b1b1ff" : "#888888ff"
                        border.width: 1
                    }

                    onAccepted: person.addRecord()
                }

                Rectangle {
                    implicitWidth: parent.height
                    implicitHeight: parent.height
                    // 半径设为宽度的一半
                    radius: implicitWidth / 2
                    color: mouseArea.containsMouse ? "#0078d4" : "#005a9e"

                    Text {
                        text: "+"
                        color: "white"
                        font.pixelSize: 20
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: person.addRecord()
                    }
                }
            }
        }
    }

    function addRecord() {
        if (inputField.text.trim() !== "") {
            personRecord.insert(0, {
                text: inputField.text,
                birthday: new Date()
            });
            inputField.text = "";
        } else {
            personRecord.insert(0, {
                text: "测试任务",
                // 5 day ago
                birthday: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
            });
            inputField.text = "";
        }
    }

    function removeRecord(index) {
        personRecord.remove(index);
    }

    function loadRecords() {
        personRecord.clear();

        // file: load from ~/data.json
        var records = []

        for (var i = 0; i < records.length; i++) {
            personRecord.append(records[i]);
        }
    }

    function dumpRecords() {
        var records = [];
        for (var i = 0; i < personRecord.count; i++) {
            records.push({
                text: personRecord.get(i).text,
                completed: personRecord.get(i).completed
            });
        }
        return records;
    }
}
