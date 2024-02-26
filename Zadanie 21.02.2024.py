import pickle

class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_address_book(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_address_book(self, filename):
        with open(filename, 'rb') as file:
            self.contacts = pickle.load(file)

    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower() or query in contact.phone_number:
                results.append(contact)
        return results

def main():
    address_book = AddressBook()

    address_book.add_contact(Contact("Karol Spiewak", "123456789"))
    address_book.add_contact(Contact("Jan Kowalski", "987654321"))

    address_book.save_address_book("address_book.pkl")

    new_address_book = AddressBook()
    new_address_book.load_address_book("address_book.pkl")

    query = input("Wyszukaj kontakty: ")
    results = new_address_book.search_contacts(query)
    if results:
        print("Znalezione kontakty:")
        for contact in results:
            print(f"Imię: {contact.name}, Numer telefonu: {contact.phone_number}")
    else:
        print("Brak pasujących kontaktów.")

if __name__ == "__main__":
    main()
