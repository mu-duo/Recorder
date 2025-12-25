from PySide6 import QtWidgets, QtCore, QtGui
from .Record import QRecord

from source.backend.Person import Person
from source.backend.Record import Record


class QRecordContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setMinimumWidth(300)

    def init_ui(self):
        self.container = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QVBoxLayout()
        self.container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.container.setLayout(self.container_layout)

        self.scroll_ = QtWidgets.QScrollArea()
        self.scroll_.setWidgetResizable(True)
        self.scroll_.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scroll_.setWidget(self.container)
        self.scroll_.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scroll_)
        self.setLayout(layout)

    def add_record(self, record: QRecord):
        self.container_layout.addWidget(record)

    def delete_record(self, record: QRecord):
        self.container_layout.removeWidget(record)
        record.setParent(None)

class QPerson(QtWidgets.QWidget):
    def __init__(self, parent=None, person=None):
        super().__init__(parent)

        if person is None:
            person = Person("Unnamed")
        self.person = person

        # ui elements
        button = QtWidgets.QPushButton("Add Record")
        button.clicked.connect(self.add_record)
        button.setFont(QtGui.QFont("Arial", 12))
        button.setFixedHeight(40)
        self.records_container = QRecordContainer()

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.records_container)
        layout.addWidget(button)
        self.setLayout(layout)

    def add_record(self):
        record_info = QRecord(self)
        record_info.set_text("content")

        self.records_container.add_record(record_info)
