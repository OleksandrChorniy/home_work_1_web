import pickle
from collections import UserDict
from abc import ABC, abstractmethod

class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

class AddressBook(UserDict):
    def add_contact(self, contact):
        self.data[contact.name] = contact.phone_number

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def search_contacts(self, search):
        result = []
        for name, phone_number in self.data.items():
            if (search.lower() in name.lower() or search in phone_number):
                result.append((name, phone_number))
        return result

class UserInterface(ABC):
    @abstractmethod
    def display_menu(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

class ConsoleUserInterface(UserInterface):
    def display_menu(self):
        print("1. Add contact.")
        print("2. Search contacts.")
        print("3. Exit.")

    def get_user_input(self, prompt):
        return input(prompt)

    def display_contacts(self, contacts):
        if contacts:
            print("Result:")
            for name, phone_number in contacts:
                print(f"Name: {name}, Phone number: {phone_number}")
        else:
            print("Sorry! No matches found.")

    def display_message(self, message):
        print(message)

def main():
    address_book = AddressBook()
    user_interface = ConsoleUserInterface()

    try:
        address_book.load_from_file('address_book.bin')
    except FileNotFoundError:
        pass

    while True:
        user_interface.display_menu()
        choice = user_interface.get_user_input("Select the option: ")

        if choice == '1':
            name = user_interface.get_user_input("Enter the name: ")
            phone_number = user_interface.get_user_input("Enter the phone number: ")
            contact = Contact(name, phone_number)
            address_book.add_contact(contact)
            address_book.save_to_file('address_book.bin')
        elif choice == '2':
            search = user_interface.get_user_input("Enter the 'name/phone': ")
            result = address_book.search_contacts(search)
            user_interface.display_contacts(result)
        elif choice == '3' or choice.lower() == 'exit':
            break
        else:
            user_interface.display_message("Oops! Please choose the correct option.")

if __name__ == "__main__":
    main()
