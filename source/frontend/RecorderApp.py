from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets, QtCore, QtGui

from source.frontend.Person import QPerson
from source.frontend.Record import QRecord
from source.backend.Person import Person
from source.backend.Record import Record


class RecorderApp_(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recorder")
        self.resize(800, 600)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QPerson(self, Person("tlf")))

    def add_person(self, person: Person):
        person_widget = QPerson(self, person)
        layout = self.layout()
        if layout is not None:
            layout.addWidget(person_widget)


class RecorderApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.recorder = RecorderApp_()

    def run(self):
        self.recorder.show()
        self.app.exec()
