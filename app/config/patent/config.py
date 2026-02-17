import toml
from typing import Dict

class TomlReader:
    def __init__(self, name: str, encoding: str = 'utf-8'):
        with open(f"app/{name}", 'r', encoding=encoding) as config:
            self.__data = toml.load(config)


class ConfigToml(TomlReader):
    def __init__(self, name = "config.toml", encoding = 'utf-8'):
        super().__init__(name, encoding)

    def form_decoder_copyright(self) -> Dict[str, str]:
        return self.__data["form_decoder_copyright"]

    def form_decoder_project(self) -> Dict[str, str]:
        return self.__data["form_decoder_project"]

    def form_decoder_author(self) -> Dict[str, str]:
        return self.__data["form_decoder_author"]


class TemplProjectToml(TomlReader):
    def __init__(self, name = "template_project.toml", encoding = 'utf-8'):
        super().__init__(name, encoding)

    def copyright_info_add(self, dct_import: Dict[str, str]) -> None:
        dct_import.update(self.__data["copyriht_info"])

    def template_data_project_add(self, dct_import: Dict[str, str]) -> None:
        dct_import.update(self.__data["template_data_project"])
