from PySide6 import QtCore, QtGui, QtWidgets

from source.backend.Record import Record


class QRecordMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(QtGui.QFont("Arial", 15))

        # 设置样式表来控制action高度
        self.setStyleSheet(
            """
            /* 控制菜单项的高度和外观 */
            QMenu::item {
                background-color: white;        /* 白色背景 */
                padding: 12px 20px;             /* 上12px 下12px | 左20px 右20px */
                margin: 0px;                    /* 无外边距 */
                border: none;                   /* 无边框 */
                height: 25px;                   /* 设置最小高度 */
                min-height: 25px;               /* 最小高度 */
                max-height: 25px;               /* 最大高度 */
                color: #202124;                 /* 深灰色文字 */
                font-size: 20px;                /* 字体大小 */
                border-radius: 8px;             /* 圆角边框 */
            }
            
            /* 鼠标悬停状态 */
            QMenu::item:selected {
                background-color: #E0E0E0;      /* 浅灰色背景 */
                color: #000000;                 /* 黑色文字 */
            }
            
            /* 禁用状态 */
            QMenu::item:disabled {
                color: #9AA0A6;                 /* 灰色文字 */
            }
            
            /* 分隔线 */
            QMenu::separator {
                height: 1px;
                background-color: #DADCE0;      /* 浅灰色分隔线 */
                margin: 4px 0px;
            }
        """
        )

        self.clear_action = QtGui.QAction(
            QtGui.QIcon.fromTheme("edit-redo"), "Reset", self
        )
        self.clear_action.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        self.addAction(self.clear_action)
        self.clear_action.setToolTip("Reset the day count to zero")

        self.delete_action = QtGui.QAction(
            QtGui.QIcon.fromTheme("edit-delete"), "Delete", self
        )
        self.addAction(self.delete_action)
        self.delete_action.setToolTip("Delete this record")

        self.setToolTipsVisible(True)


class QRecord(QtWidgets.QWidget):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)

        # data
        if record is None:
            record = Record.test()
        self.record = record

        # ui
        self.bg_color = QtGui.QColor(250, 250, 250)
        self.text_color = QtGui.QColor(0, 0, 0)
        self.shadow_color = QtGui.QColor(0, 0, 0, 50)

        self.padding = 10
        self.border_radius = 15

        # font
        self.setFont(QtGui.QFont("Arial", 12))
        self.font().setBold(True)

        self.setMinimumHeight(80)
        self.setMinimumWidth(100)

        self.setMaximumHeight(100)

    def set_text(self, text):
        self.record.content = text

    # 鼠标悬浮高亮显示
    def enterEvent(self, event):
        self.bg_color = QtGui.QColor(200, 200, 200)
        self.update()

    def leaveEvent(self, event):
        self.bg_color = QtGui.QColor(250, 250, 250)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        try:
            # draw background
            painter.setBrush(self.bg_color)
            painter.setPen(QtGui.QPen(self.bg_color, 1))
            painter.drawRoundedRect(self.rect(), self.border_radius, self.border_radius)

            # left: text, right: day number
            rect = self.rect()
            painter.setFont(self.font())
            painter.setPen(self.text_color)
            day_number_rect = QtCore.QRect(
                rect.right() - 100 - self.padding,
                rect.top() + self.padding,
                100,
                rect.height() - 2 * self.padding,
            )
            text_rect = QtCore.QRect(
                rect.left() + self.padding,
                rect.top() + self.padding,
                rect.width() - 120 - 2 * self.padding,
                rect.height() - 2 * self.padding,
            )
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self.record.content,
            )
            painter.drawText(
                day_number_rect,
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                f"Day {self.record.calculate_day_count()}",
            )
        except Exception as e:
            print(f"Error in paintEvent: {e}")
        painter.end()

    def contextMenuEvent(self, event):
        menu = QRecordMenu(self)
        action = menu.exec(event.globalPos())
        if action == menu.delete_action:
            self.delete_record()
        elif action == menu.clear_action:
            self.record.reset()
            self.update()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.record.content += " (edited)"
        self.update()
        return super().mouseDoubleClickEvent(event)

    def delete_record(self):
        parent = self.parent()
        if isinstance(parent, QtWidgets.QWidget):
            parent_layout = parent.layout()
            if parent_layout is not None:
                parent_layout.removeWidget(self)
        self.setParent(None)
        self.deleteLater()
