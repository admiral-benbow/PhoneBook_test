from Contact import Contact
import os


class PhoneBook:
    project_folder = os.path.realpath("..")
    db_file_name = "data_base.txt"
    __DB_FILE = os.path.join(project_folder, db_file_name)

    def add_contact(self, contact: Contact=None):
        with open(self.__DB_FILE, mode="a", encoding="utf-8") as file:
            file.write("bubba")


if __name__ == '__main__':

    stone = Contact(
        name="Kirill",
        surname="Chechkin",
        patronymic="Victorovich",
        organization="geologist",
        work_number="+88005553535",
        private_number="+79603208063"
    )

    PhoneBook().add_contact()
