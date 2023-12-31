class Contact:
    """
     Класс для описания единичной записи контакта (без уникального ID)

     Класс для хранения получаемых данных от пользователя, в целях дальнейшего сохранения данных контакта
     в базе данных. Также для удобного вывода в строковом представлении
    """
    def __init__(self, name: str,
                 surname: str,
                 patronymic: str,
                 organization: str,
                 work_number: str,
                 private_number: str):
        self.__name = name
        self.__surname = surname
        self.__patronymic = patronymic
        self.__organization = organization
        self.__work_number = work_number
        self.__private_number = private_number

    def __str__(self):
        return f"Абонент: {self.surname} {self.name} {self.patronymic}, Организация: {self.organization}\n" \
               f"Раб. телефон: {self.work_number}, Личный телефон: {self.private_number}"

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def surname(self) -> str:
        return self.__surname

    @surname.setter
    def surname(self, new_surname: str) -> None:
        self.__surname = new_surname

    @property
    def patronymic(self) -> str:
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, new_patronymic: str) -> None:
        self.__patronymic = new_patronymic

    @property
    def organization(self) -> str:
        return self.__organization

    @organization.setter
    def organization(self, new_organization: str) -> None:
        self.__organization = new_organization

    @property
    def work_number(self) -> str:
        return self.__work_number

    @work_number.setter
    def work_number(self, new_work_number: str) -> None:
        self.__work_number = new_work_number

    @property
    def private_number(self) -> str:
        return self.__private_number

    @private_number.setter
    def private_number(self, new_private_number: str) -> None:
        self.__private_number = new_private_number
