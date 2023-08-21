from classes.Contact import Contact
import os


project_folder = os.path.realpath("..")
db_file_name = "data_base.txt"
DB_FILE = os.path.join(project_folder, db_file_name)


class PhoneBook:
    """
    Класс, описывающий интерфейс для работы с телефонным справочником
    """
    def __init__(self, db_file: str):
        self.__db_file = db_file

    def menu(self) -> None:
        """
        Вывод главного меню телефонного справочника в консоль
        """
        while True:
            print("Главное меню телефонного справочника. Выберете действие (введите цифру): ")
            print("1 - Открыть контакты по одному\n"
                  "2 - Открыть контакты группой по страницам\n"
                  "3 - Добавить новый контакт\n"
                  "0 - закончить работу")

            user_choice = int(input(""))

            if user_choice == 1:
                self.get_contacts_one()
                print("Контакт добавлен!")

            elif user_choice == 2:
                user_page_choice = input("Желаете ли выбрать длину списка? По умолчанию - 5 (Y/N): ").lower()
                if user_page_choice == "y":
                    user_num_choice = input("Введите длину списка контактов на странице (больше 0): ")
                    try:
                        user_num_choice = int(user_num_choice)
                    except ValueError:
                        print("Введено не число. Пожалуйста, попытайтесь заново и введите число")
                    if user_num_choice > 0:
                        self.get_contacts_pages(length=user_num_choice)
                    else:
                        print("Введено неверное значение. Пожалуйста, попытайтесь заново и введите число больше нуля")
                elif user_page_choice == "n":
                    self.get_contacts_pages()
                else:
                    print("Неизвестная команда. Возвращаемся в главное меню")

            elif user_choice == 3:
                self.add_contact()
                print("Контакт добавлен!")
            elif user_choice == 0:
                print("Спасибо за использование справочника")
                break
            else:
                print("Неизвестная команда. Введите действие (цифру) снова")

    def add_contact(self) -> None:
        """Создание класса Contact, вытягивание из него информации и запись её в 'базу данных'.txt"""

        new_contact = Contact(
            name=input("Введите имя: "),
            surname=input("Введите фамилию: "),
            patronymic=input("Введите отчество: "),
            organization=input("Введите организацию: "),
            work_number=input("Введите рабочий номер: "),
            private_number=input("Введите личный номер: ")

        )

        try:
            with open(self.__db_file, mode="a+", encoding="utf-8") as file:
                file.write(f"{new_contact.name}|{new_contact.surname}|{new_contact.patronymic}|"
                           f"{new_contact.organization}|{new_contact.work_number}|{new_contact.private_number}\n")
        except FileNotFoundError:
            print("Что-то пошло не так. Обратитесь к разработчику за дополнительной информацией, всё скоро починят!")

    def get_contacts_one(self):
        """Интерфейс просмотра контактов по одному"""

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
                    print("Возвращаемся в главное меню")
                    break
                else:
                    print("Неизвестная команда")

    def get_contacts_pages(self, length: int = 5) -> None:
        """
        Выводит контакты из справочника в консоль в виде списка постранично
        Длина каждой страницы может регулироваться пользователем
        """

        with open(self.__db_file, mode="r", encoding="utf-8") as file:
            contacts_by_line = file.readlines()

            contacts_pages_dict = {

            }
            page_cnt = 1
            volume_cnt = 0
            for i_contact in contacts_by_line:
                volume_cnt += 1
                if volume_cnt > length:
                    page_cnt += 1
                    volume_cnt = 1

                reformed_contact = i_contact.strip("\n").split("|")
                contact = Contact(reformed_contact[0], reformed_contact[1], reformed_contact[2],
                                  reformed_contact[3], reformed_contact[4], reformed_contact[5])
                if not contacts_pages_dict.get(page_cnt):
                    contacts_pages_dict[page_cnt] = []
                    contacts_pages_dict[page_cnt].append(contact)
                else:
                    contacts_pages_dict[page_cnt].append(contact)

            view_pages_cnt = 1
            while view_pages_cnt < page_cnt + 1:
                print(f"Страница контактов #{view_pages_cnt}\n")
                for j_contact in contacts_pages_dict[view_pages_cnt]:
                    print(j_contact, "\n")

                user_choice = int(input("Далее - 1;\nНазад - 2;\nЗакончить - 3;\nВвод: "))
                print()

                if user_choice == 1:
                    view_pages_cnt += 1
                    if view_pages_cnt > len(contacts_pages_dict):
                        print("Это последняя страница")
                        view_pages_cnt -= 1
                elif user_choice == 2:
                    view_pages_cnt -= 1
                    if view_pages_cnt < 1:
                        print("Это самая первая страница")
                        view_pages_cnt += 1
                elif user_choice == 3:
                    print("Возвращаемся в главное меню")
                    break
                else:
                    print("Неизвестная команда")

    def check_contact_line(self):
        """Заглушка - ф-ция, если я захочу вводить ID-номера контактов"""
        pass


if __name__ == '__main__':
    # PhoneBook(DB_FILE).add_contact()
    # PhoneBook(DB_FILE).get_contacts_one()
    PhoneBook(DB_FILE).get_contacts_pages()
