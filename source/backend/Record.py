import datetime

class Record:
    def __init__(self, parent=None, content=""):
        self.parent = parent
        self.content = content

        # get the date form now
        self.birth_date = datetime.datetime.now().date()

    def calculate_day_count(self):
        today = datetime.datetime.now().date()
        delta = today - self.birth_date
        return delta.days
    
    def reset(self):
        self.birth_date = datetime.datetime.now().date()

    def get_parent(self):
        return self.parent

    @staticmethod
    def test():
        record = Record()
        record.birth_date = datetime.datetime.now().date() - datetime.timedelta(days=5)
        record.content = "Test Record"
        return record