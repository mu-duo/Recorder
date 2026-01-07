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
