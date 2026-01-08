import datetime


class Record:
    def __init__(self, parent=None, content=""):
        self.content = content

        # get the date form now
        self.birth_date = datetime.datetime.now().date()

    def calculate_day_count(self):
        today = datetime.datetime.now().date()
        delta = today - self.birth_date
        return delta.days

    def reset(self):
        self.birth_date = datetime.datetime.now().date()

    @staticmethod
    def GenerateNewRecord():
        record = Record()
        record.birth_date = datetime.datetime.now().date()
        record.content = "Test Record"
        return record

    @classmethod
    def load(cls, data):
        record = cls()
        record.content = data.get("content", "")
        birth_date_str = data.get("birth_date", "")
        try:
            record.birth_date = datetime.datetime.strptime(
                birth_date_str, "%Y-%m-%d"
            ).date()
        except ValueError:
            record.birth_date = datetime.datetime.now().date()
        return record

    def save(self):
        return {
            "content": self.content,
            "birth_date": self.birth_date.strftime("%Y-%m-%d"),
        }
