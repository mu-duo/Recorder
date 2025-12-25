from source.backend.Record import Record

class Person:
    def __init__(self, name):
        self.name = name
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)
