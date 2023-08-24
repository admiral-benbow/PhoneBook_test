from classes.PhoneBook import PhoneBook
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(root_dir, "data_base.txt")


if __name__ == '__main__':
    phonebook = PhoneBook(db_file=DB_PATH)
    phonebook.menu()


# Notes:
# Сделать проверку на пустое поле
