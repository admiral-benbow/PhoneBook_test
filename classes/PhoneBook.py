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
        # Создаём сценарий для ввода информации по контакту

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


if __name__ == '__main__':
    PhoneBook(DB_FILE).add_contact()

