from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets, QtCore, QtGui

from source.frontend.Person import QPerson
from source.frontend.Record import QRecord
from source.backend.RecordMgr import RecordMgr
from source.backend.Person import Person
from source.backend.Record import Record


class SaveThread(QtCore.QThread):
    def __init__(self, manager: RecordMgr, parent=None):
        super().__init__(parent)
        self.manager = manager

    def run(self):
        while True:
            self.manager.save()
            self.msleep(60000)  # Save every 60 seconds


class RecorderApp_(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recorder")
        self.resize(800, 600)
        self.manager = RecordMgr()
        self.manager.load()
        self.save_thread = SaveThread(self.manager)
        self.save_thread.start()

        self.init_ui()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.save_thread.terminate()
        self.manager.save()
        return super().closeEvent(event)

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.mune = QtWidgets.QMenuBar(self)
        layout.addWidget(self.mune)
        layout.addWidget(self.tabWidget)

        button = QtWidgets.QPushButton("Add Person")
        button.setFont(QtGui.QFont("Arial", 12))
        button.setFixedHeight(40)
        button.clicked.connect(self.add_person)
        layout.addWidget(button)

        if not self.manager.persons:
            self.manager.persons.append(Person("Default Person"))

        for person in self.manager.persons:
            self.tabWidget.addTab(QPerson(self, person), person.name)

    def add_person(self):
        person = Person("New Person")
        self.manager.add_person(person)
        person_tab = QPerson(self, person)
        self.tabWidget.addTab(person_tab, person.name)
        self.tabWidget.setCurrentWidget(person_tab)


class RecorderApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.recorder = RecorderApp_()

    def run(self):
        self.recorder.show()
        self.app.exec()
