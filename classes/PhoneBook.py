import re
import os

from classes.Contact import Contact


project_folder = os.path.realpath("..")
db_file_name = "data_base.txt"
DB_FILE = os.path.join(project_folder, db_file_name)


class PhoneBook:
    """
    Класс, описывающий интерфейс и функционал телефонного справочника
    """

    def __init__(self, db_file: str):
        self.__db_file = db_file

    @property
    def db_file(self) -> str:
        return self.__db_file

    def menu(self) -> None:
        """
        Вывод главного меню телефонного справочника в консоль, где вызываются все остальные методы класса
        """

        while True:
            print("Главное меню телефонного справочника. Выберете действие (введите цифру): ")
            print("1 - Открыть контакты по одному\n"
                  "2 - Открыть контакты группой по страницам\n"
                  "3 - Добавить новый контакт\n"
                  "4 - Найти контакт в справочнике\n"
                  "0 - закончить работу\n")

            try:
                user_choice = int(input("Ввод: "))
                print()
            except ValueError:
                print("Неизвестная команда. Возврат к началу")
                continue

            if user_choice == 1:
                self.get_contacts_one()

            elif user_choice == 2:
                user_page_choice = input("Желаете ли выбрать длину списка? По умолчанию длина - 5\n"
                                         "Введите 'Y', чтобы выбрать самостоятельно,"
                                         "'N' - чтобы оставить по умолчанию\n"
                                         "Ввод: ").lower()
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
            elif user_choice == 4:
                self.find_contact()
            elif user_choice == 0:
                print("Спасибо за использование справочника")
                break
            else:
                print("Неизвестная команда. Введите действие (цифру) снова")

    def add_contact(self) -> None:
        """Добавление записи нового контакта в 'базу данных'.txt"""

        new_contact = Contact(
            name=input("Введите имя: "),
            surname=input("Введите фамилию: "),
            patronymic=input("Введите отчество: "),
            organization=input("Введите организацию: "),
            work_number=input("Введите рабочий номер: "),
            private_number=input("Введите личный номер: ")

        )
        print()

        try:
            with open(self.__db_file, mode="r", encoding="utf-8") as file:
                try:
                    last_contact_num = int(file.readlines()[-1].split("|")[0]) + 1
                except IndexError:
                    last_contact_num = 1
        except (FileNotFoundError, FileExistsError):
            print("Что-то пошло не так. Обратитесь к разработчику за дополнительной информацией, всё скоро починят!")
            return

        try:
            with open(self.__db_file, mode="a+", encoding="utf-8") as file:
                file.write(f"{last_contact_num}|{new_contact.name}|{new_contact.surname}|{new_contact.patronymic}|"
                           f"{new_contact.organization}|{new_contact.work_number}|{new_contact.private_number}\n")
                print("Контакт добавлен!\n")
        except (FileNotFoundError, FileExistsError):
            print("Что-то пошло не так. Обратитесь к разработчику за дополнительной информацией, всё скоро починят!")

    def get_contacts_one(self) -> None:
        """Метод для просмотра записей контактов по одному. Также на странице контакта переход к его редактированию"""

        continue_from_edited_contact = False
        while True:

            with open(self.__db_file, mode="r", encoding="utf-8") as file:
                contacts_by_line = file.readlines()

            if not continue_from_edited_contact:
                i_contact = 0
            else:
                continue_from_edited_contact = False

            while i_contact < len(contacts_by_line):
                contact_list = contacts_by_line[i_contact].strip("\n").split("|")

                id_contact = contact_list[0]
                contact = Contact(contact_list[1], contact_list[2], contact_list[3],
                                  contact_list[4], contact_list[5], contact_list[6])

                print(contact, '\n')
                try:
                    user_choice = int(input("Далее - 1;\nНазад - 2;\nРедактирование - 3\nЗакончить - 4;\nВвод: "))
                    print()
                except ValueError:
                    print("Неверная команда. Возврат к началу выбора контактов по одному на страницу")
                    continue

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
                    if self.edit_contact(id_contact=id_contact):
                        continue_from_edited_contact = True
                        break
                elif user_choice == 4:
                    print("Возвращаемся в главное меню")
                    return
                else:
                    print("Неизвестная команда")

    def get_contacts_pages(self, length: int = 5) -> None:
        """
        Выводит контакты из справочника в консоль в виде списка постранично
        Длина каждой страницы может регулироваться пользователем.
        :param length -> int - длина каждой страницы (по ум. 5)
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
                contact = Contact(reformed_contact[1], reformed_contact[2], reformed_contact[3],
                                  reformed_contact[4], reformed_contact[5], reformed_contact[6])
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

    def edit_contact(self, id_contact: str) -> bool | None:
        """
        Метод для изменения записи контакта в базе данных
        :param id_contact: str -> строковое представление уникального id контакта из "базы_данных".txt
        :return: True, если контакт успешно изменён | None, если редактирования не произошло
        """

        edit_contact_menu = (None, "Имя", "Фамилию", "Отчество", "Организацию", "Рабочий телефон", "Личный телефон")
        rus_suffixes = (None, "ое", "ую", "ое", "ую", "ый", "ый")

        while True:
            print("Что желаете отредактировать?\n"
                  f"1 - {edit_contact_menu[1]}\n"
                  f"2 - {edit_contact_menu[2]}\n"
                  f"3 - {edit_contact_menu[3]}\n"
                  f"4 - {edit_contact_menu[4]}\n"
                  f"5 - {edit_contact_menu[5]}\n"
                  f"6 - {edit_contact_menu[6]}\n"
                  f"7 - Отмена")
            try:
                user_choice = int(input("Ваш ввод: "))
            except ValueError:
                print("Неизвестная команда. Попробуйте снова")
                continue

            if user_choice in range(1, 7):
                break
            elif user_choice == 7:
                return
            else:
                print("Неизвестная команда. Введите команду заново")

        user_edit_input = input(f"Введите нов{rus_suffixes[user_choice]} {edit_contact_menu[user_choice]}: ")
        with open(self.db_file, mode="r", encoding="utf-8") as file:
            all_contacts = file.readlines()
            for i_contact in all_contacts:
                if i_contact.split("|")[0] == id_contact:
                    editing_contact_list = all_contacts[int(id_contact) - 1].split("|")
                    editing_contact_list[user_choice] = user_edit_input
                    all_contacts[int(id_contact) - 1] = "|".join(editing_contact_list)
        with open(self.db_file, mode="w+", encoding="utf-8") as file:
            for j_contact in all_contacts:
                file.write(j_contact)
            return True

    def find_contact(self) -> None:
        """Поиск по контактам в "базе_данных".txt по одному или нескольким (до всех) критериям"""

        finding_param_tuple = (None, "имя", "фамилию", "отчество", "организацию", "рабочий телефон", "личный телефон")
        at_least_one_found = False
        # Menu-part
        print("Поиск по контактам. Введите комбинацию цифр для поиска контактов\n"
              "Можно выбрать любое сочетание (одна или несколько цифр):\n"
              "1 - по имени\n"
              "2 - по фамилии\n"
              "3 - по отчеству\n"
              "4 - по организации\n"
              "5 - по рабочему телефону\n"
              "6 - по личному  телефону \n"
              "7 - отмена. Вернуться назад\n")

        user_choice = input("Ввод: ")

        if user_choice.isdigit():
            if user_choice == "7":
                return
            else:
                choice_input_tuple = tuple(map(int, user_choice))

        else:
            print("Incorrect command")
            return

        with open(self.db_file, mode="r", encoding="utf-8") as file:
            all_contacts = file.readlines()

        finding_params_list = []
        for j_match in choice_input_tuple:
            user_param_input = input(f"Введите {finding_param_tuple[j_match]} ").lower()
            print()
            finding_params_list.append(user_param_input)

        for i_contact in all_contacts:
            a_contact_list = i_contact.strip("\n").split("|")
            contact_class = Contact(
                name=a_contact_list[1],
                surname=a_contact_list[2],
                patronymic=a_contact_list[3],
                organization=a_contact_list[4],
                work_number=a_contact_list[5],
                private_number=a_contact_list[6],
            )

            for k_index, k_pattern in zip(choice_input_tuple, finding_params_list):
                if k_index in (5, 6):
                    if "+" in k_pattern:
                        re_pattern = f"\\{k_pattern}"
                    else:
                        re_pattern = f"{k_pattern}"
                else:
                    re_pattern = f"^{k_pattern.lower()}"

                match = re.search(re_pattern, a_contact_list[k_index].lower())

                if not match:
                    break
            else:
                print(str(contact_class))
                print()
                at_least_one_found = True

        if not at_least_one_found:
            print("Контактов с таким(и) параметром(ами) не найдено")
            print()
