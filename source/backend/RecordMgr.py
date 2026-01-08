import json
from pathlib import Path

from source.backend.Person import Person


class RecordMgr:
    DEFAULT_DATA_FILE = Path("~/data.json").expanduser()
    def __init__(self):
        self.persons = []

    def add_person(self, person):
        self.persons.append(person)

    def remove_person(self, person):
        self.persons.remove(person)

    def load(self, data_file=None):
        if data_file is None:
            data_file = self.DEFAULT_DATA_FILE

        if not Path(data_file).exists():
            print(f"Data file {data_file} does not exist. Starting with empty data.")
            return
        else:
            print(f"Loading data from {data_file}")

        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for person_data in data.get("persons", []):
                person = Person.load(person_data)
                self.persons.append(person)
        except Exception as e:
            print(f"Failed to load data from {data_file}: {e}")

    def save(self, data_file=None):
        if data_file is None:
            data_file = self.DEFAULT_DATA_FILE

        data = {"persons": []}
        for person in self.persons:
            person_data = person.save()
            data["persons"].append(person_data)

        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"data: {data}")

