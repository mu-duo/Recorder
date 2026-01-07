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
            record.birth_date = record_data.get("birth_date", record.birth_date)
            ret.records.append(record)

        return ret

    def save(self):
        data = {"name": self.name, "records": []}
        for record in self.records:
            record_data = {"content": record.content, "birth_date": record.birth_date}
            data["records"].append(record_data)
        return data
