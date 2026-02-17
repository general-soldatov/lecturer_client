import random
from pydantic import BaseModel
from typing import List, Dict
from .configure import YamlProject

class ObjectTicket(BaseModel):
    count: int
    category: Dict[int, List[str]]

class ConfigTicket(BaseModel):
    study: Dict[str, str]
    ticket: ObjectTicket

class TicketTemp(YamlProject):
    configure: ConfigTicket
    question: Dict[str, List[str]]

    def export_question(self, not_keys = ['tasks']):
        return [elem for key, value in self.question.items()
                if key not in not_keys for elem in value]


class TicketOutput(BaseModel):
    learn_year: str
    department: str
    faculty: str
    direct: str
    course: str
    discipline: str
    questions: List[Dict[int, str]]
    ticket_count: int

    @staticmethod
    def question_to_list(ticket_data: TicketTemp, number: int, count_question: int):
        question = []
        for tick in ticket_data.configure.ticket.category[number]:
            question.extend(ticket_data.question[tick])
        random.shuffle(question)
        if not count_question:
            count_question = ticket_data.configure.ticket.count
        count = count_question - len(question)
        if count > 0:
            question.extend((random.choice(question) for _ in range(count)))
        return question[:count_question]

    @classmethod
    def model_construct(cls, ticket_data: TicketTemp, _fields_set = None, **values):
        data: List[Dict[int, str]] = [{key: key for key in ticket_data.configure.ticket.category.keys()}
                                      for _ in range(ticket_data.configure.ticket.count)]

        if ticket_data.configure.ticket.category[1] == ticket_data.configure.ticket.category[2]:
            count_question = ticket_data.configure.ticket.count * 2
            list_of_questions = cls.question_to_list(ticket_data, 1, count_question)
            question = {
                1: list_of_questions[:ticket_data.configure.ticket.count],
                2: list_of_questions[ticket_data.configure.ticket.count:],
                3: cls.question_to_list(ticket_data, 3, ticket_data.configure.ticket.count)
            }
        else:
            question = {key: cls.question_to_list(ticket_data, key, ticket_data.configure.ticket.count)
                        for key, _ in ticket_data.configure.ticket.category.items()}
        for key, _ in ticket_data.configure.ticket.category.items():
            for i, elem in enumerate(question[key]):
                data[i][key] = elem
        return cls(
            ticket_count=ticket_data.configure.ticket.count,
            questions=data,
            **ticket_data.configure.study
        )
