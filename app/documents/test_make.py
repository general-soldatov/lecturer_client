import yaml
from typing import List, Dict, Union
from pydantic import BaseModel, ConfigDict
from enum import Enum

class QuestionsType(Enum):
    """Типы вопросов"""
    CHOICE = "choice"                    # Несколько правильных ответов
    MATCHING = "matching"                # Сопоставление
    SORTING = "sorting"                  # Сортировка
    NUMBER = "number"

class YamlProject(BaseModel):
    @classmethod
    def model_validate_yaml(cls, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as file:
            data = yaml.safe_load(file.read())
            return cls.model_validate(data)

class Question(BaseModel):
    types: str
    text_data: str
    code_path: str | None = None
    image: str | None = None
    help: str | None = None


class AnswerTest(BaseModel):
    correct: List[str]
    wrong: List[str]

class AnswerMatching(BaseModel):
    first: List[str]
    second: List[str]

class AnswerSorting(BaseModel):
    steps: List[str]

class OptionNumber(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    answer: str = '0'
    max_error: str = '0'

class SourceString(BaseModel):
    pattern: str
    use_re: bool
    match_substring: bool
    case_sensitive: bool
    code: str
    is_text_disabled: bool
    is_file_disabled: bool

class AnswerNumber(BaseModel):
    data: List[OptionNumber]

class TaskTemplate(YamlProject):
    question: Question
    answer: Union[AnswerTest, AnswerMatching, AnswerSorting, AnswerNumber, SourceString]

class Elems(BaseModel):
    name: str
    theory: List[str]
    tasks: List[TaskTemplate]

class Project(BaseModel):
    elems: List[Elems]

    @staticmethod
    def read(path: str):
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file.read())

    @classmethod
    def open_project(cls, path: str):
        return cls(elems = cls.read(path))
