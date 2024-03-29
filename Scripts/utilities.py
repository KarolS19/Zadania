import pickle
from classes import AddressBook
import json

def load_default_contacts(address_book: AddressBook, exists = False):
    if not exists:
        with open("default_contacts.json", "r") as rff:
            random_contacts =  json.load(rff)
        for person in random_contacts:
            address_book.add_contact(person['name'])
            address_book.contacts[person['name']].add_phone(person['phone'])
            address_book.contacts[person['name']].add_email(person['email'])
            address_book.contacts[person['name']].add_birthday(person['birthday'])
            address_book.contacts[person['name']].add_address(person['address'])
    return address_book

def load_from_file():
    try:
        with open('bot_save.bin',"rb") as fh:
            address_book = pickle.load(fh)
            print('The adress_book has been loaded from file')
    except FileNotFoundError:
        print("File with address_book doesn't exist yet! Creating new Addressbook")
        address_book = AddressBook()
        address_book = load_default_contacts(address_book)
        return address_book
    return address_book