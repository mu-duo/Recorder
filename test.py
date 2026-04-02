import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon


def main():
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"
    app = QApplication(sys.argv)

    # 创建 QQuickView
    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)

    # 加载 Person.qml 文件
    qml_file = QUrl.fromLocalFile("source/frontend/Person.qml")
    view.setSource(qml_file)

    # 设置窗口属性
    view.setTitle("Person Record")
    view.setMinimumWidth(400)
    view.setMinimumHeight(600)
    view.resize(400, 600)

    # 设置图标
    icon = QIcon("source/imgs/icon.png")
    app.setWindowIcon(icon)

    # 系统托盘图标
    tray_icon = QSystemTrayIcon(icon, app)
    tray_icon.setToolTip("Person Record")
    tray_icon.show()

    # 显示窗口
    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
