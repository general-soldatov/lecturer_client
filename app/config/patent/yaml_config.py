import yaml
from typing import Dict
from datetime import date

class YamlCreator:
    def __init__(self, path: str, encoding: str = 'utf-8'):
        self._path = path
        with open(path, 'r', encoding=encoding) as project:
            self._data = yaml.safe_load(project)

    def recording(self, path: str = None, encoding: str = 'utf-8'):
        if not path:
            path = self._path
        with open(path, 'w', encoding=encoding) as project:
            yaml.dump(self._data, project)

class ProjectReader(YamlCreator):
    def __init__(self, path, encoding = "utf-8"):
        super().__init__(path, encoding)

    @staticmethod
    def _full_name(author: Dict[str, str]):
        return f"{author['first_name']} {author['name']} {author['last_name']}"

    def copyright_info_add(self, dct_import: Dict[str, str]) -> None:
        dct_import.update(self._data["copyright_info"])

    def program_info_add(self, dct_import: Dict[str, str]) -> None:
        dct_import.update(self._data["info_program"])

    def author_info_add(self, dct_import: Dict[str, str], num_author: int = 1) -> None:
        author: Dict[str, str] = self._data["info_authors"][f"author_{num_author}"]
        dct_import["full_name"] = self._full_name(self._data["info_authors"][f"author_{num_author}"])
        dct_import["full_address"] = author["full_address"]
        dct_import["citizenship"] = author["citizenship"]
        dates: str = date.fromisoformat(author['pasport_date']).strftime("%d.%m.%Y")
        dct_import["passport_data"] = f"{author['passport_series']} {author['passport_number']}, выдан {author['pasport_organisation'].strip()}, {dates}"

    def author_full_info_add(self, dct_import: Dict[str, str], num_author: int = 1) -> None:
        self.author_info_add(dct_import, num_author)
        author: Dict[str, str] = self._data["info_authors"][f"author_{num_author}"]
        dates: date = date.fromisoformat(str(author['date_of_birth']))
        dct_import["day_birth"] = "{:02d}".format(dates.day)
        dct_import["month_birth"] = "{:02d}".format(dates.month)
        dct_import["year_birth"] = dates.year
        dct_import["name_of_prog"] = self._data["info_program"]["name_of_prog"]

    def authorConsentOne(self, num_author: int = 1) -> Dict[str, str]:
        data_author = dict()
        self.author_info_add(data_author, num_author)
        data_author["name_of_prog"] = self._data["info_program"]["name_of_prog"]
        return data_author

    def authorConsentTwo(self, num_author: int = 1) -> Dict[str, str]:
        data_author = dict()
        self.author_full_info_add(data_author, num_author)
        self.copyright_info_add(data_author)
        today: date = date.today()
        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        data_author["today"] = "«{:02d}» {} {} г.".format(today.day,
                                                              months[today.month - 1], today.year)
        return data_author

    def reportOfPatent(self) -> Dict[str, str]:
        data_author: Dict[str, str] = dict()
        data_author.update(self._data["info_program"])
        data_author["full_name"] = self._full_name(self._data["info_authors"]["author_1"])
        data_author["copyright_holder"] = self._data["copyright_info"]["copyright_holder"]
        data_author["name_of_prog"] = data_author["name_of_prog"].upper()
        data_author["authors"] = ", ".join([self._full_name(value)
                                        for _, value in self._data["info_authors"].items()])
        return data_author

    def dataOfAutors(self) -> Dict[str, str]:
        data_author: Dict[str, str] = dict()
        data_author["full_name"] = self._full_name(self._data["info_authors"]["author_1"])
        data_author["name_of_prog"] = self._data["info_program"]["name_of_prog"].upper()
        data_author["authors"] = []
        for _, value in self._data["info_authors"].items():
            data_dct = {}
            data_dct["full_name"] = self._full_name(value)
            data_dct["citizenship"] = value["citizenship"]
            data_dct["date_of_birth"] = date.fromisoformat(str(value["date_of_birth"])).isoformat()
            data_dct["full_address"] = value["full_address"]
            data_author["authors"].append(data_dct)

        return data_author

    def programTitle(self) -> Dict[str, str]:
        data_author: Dict[str, str] = dict()
        data_author["full_name"] = self._full_name(self._data["info_authors"]["author_1"])
        data_author["name_of_prog"] = self._data["info_program"]["name_of_prog"].upper()
        data_author["authors"] = [self._full_name(value) for _, value in self._data["info_authors"].items()]
        data_author["copyright_holder"] = self._data["copyright_info"]["copyright_holder"]
        data_author["program_text"] = self._data["info_program"]["program_text"]
        data_author["count_list"] = self._data["info_program"]["count_list"]

        return data_author


if __name__ == "__main__":
    data = ProjectReader("examples/project_1.yaml")
    print(data.dataOfAutors())
