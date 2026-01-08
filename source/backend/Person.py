from datetime import datetime
from source.backend.Record import Record


class Person:
    def __init__(self, name):
        self.name = name
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    @classmethod
    def load(cls, data):
        ret = cls(data.get("name", "Unnamed"))

        records_data = data.get("records", [])
        for record_data in records_data:
            record = Record(parent=ret, content=record_data.get("content", ""))
            birth_date = record_data.get("birth_date", record.birth_date)
            if isinstance(birth_date, (str,)):
                try:
                    record.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
                except ValueError:
                    record.birth_date = datetime.now().date()
            ret.records.append(record)

        return ret

    def save(self):
        data = {"name": self.name, "records": []}
        for record in self.records:
            record: Record
            birth_date = record.birth_date
            if isinstance(birth_date, (str,)):
                birth_date_str = birth_date
            else:
                birth_date_str = birth_date.strftime("%Y-%m-%d")

            record_data = {"content": record.content, "birth_date": birth_date_str}
            data["records"].append(record_data)
        return data
