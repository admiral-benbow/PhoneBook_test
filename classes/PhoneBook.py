from classes.Contact import Contact
import os


project_folder = os.path.realpath("..")
db_file_name = "data_base.txt"
DB_FILE = os.path.join(project_folder, db_file_name)


class PhoneBook:
    def __init__(self, db_file: str):
        self.__db_file = db_file

    def menu(self) -> None:
        """
        Вывод условного пользовательского интерфейса в консоль
        """
        while True:
            print("Главное меню телефонного справочника. Выберете действие (введите цифру): ")
            print("1 - добавить контакт\n"
                  "0 - закончить работу")

            user_choice = int(input(""))

            if user_choice == 1:
                self.add_contact()
                print("Контакт добавлен!")
            elif user_choice == 0:
                print("Спасибо за использование справочника")
                break

    def add_contact(self):
        """Создать класс нового контакта и добавить его в справочник"""

        new_contact = Contact(
            name=input("Введите имя: "),
            surname=input("Введите фамилию: "),
            patronymic=input("Введите отчество: "),
            organization=input("Введите организацию: "),
            work_number=input("Введите рабочий номер: "),
            private_number=input("Введите личный номер: ")

        )

        with open(self.__db_file, mode="a+", encoding="utf-8") as file:
            file.write(f"{new_contact.name}|{new_contact.surname}|{new_contact.patronymic}|"
                       f"{new_contact.organization}|{new_contact.work_number}|{new_contact.private_number}\n")

    def get_contacts_one(self):
        """Var. 2 - by one contact at a time -> through !While-loop!"""

        with open(self.__db_file, mode="r", encoding="utf-8") as file:
            contacts_by_line = file.readlines()

            i_contact = 0
            while i_contact < len(contacts_by_line):
                contact_list = contacts_by_line[i_contact].strip("\n").split("|")

                contact = Contact(contact_list[0], contact_list[1], contact_list[2],
                                  contact_list[3], contact_list[4], contact_list[5])

                print(contact, '\n')
                user_choice = int(input("Далее - 1;\nНазад - 2;\nЗакончить - 3;\nВвод: "))
                if user_choice == 1:
                    i_contact += 1
                    if i_contact == len(contacts_by_line):
                        print("Это последний контакт. Возвращаемся назад")
                        i_contact -= 1
                elif user_choice == 2:
                    i_contact -= 1
                    if i_contact < 0:
                        print("Это и есть самый первый контакт")
                        i_contact += 1
                elif user_choice == 3:
                    break
                else:
                    print("Неизвестная команда")


    def check_contact_line(self):
        """Заглушка - ф-ция, если я захочу вводить ID-номера контактов"""
        pass


if __name__ == '__main__':
    # PhoneBook(DB_FILE).add_contact()
    # PhoneBook(DB_FILE).get_contacts_1()
    PhoneBook(DB_FILE).get_contacts_one()
