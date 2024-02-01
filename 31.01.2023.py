from datetime import datetime, timedelta

class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        # Dodaj logikę walidacji numeru telefonu
        pass


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        # Dodaj logikę walidacji daty urodzin
        pass


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def __iter__(self):
        return iter(self.records)


# Przykład użycia:

address_book = AddressBook()

record1 = Record("John Doe", "123-456-7890", datetime(1990, 5, 20))
record2 = Record("Jane Smith", "987-654-3210")

address_book.add_record(record1)
address_book.add_record(record2)

for record in address_book:
    print(f"Name: {record.name.value}, Phone: {record.phone.value}")
    if record.birthday:
        print(f"Days to Birthday: {record.days_to_birthday()}")

