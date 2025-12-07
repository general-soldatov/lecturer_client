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
    def question_to_list(ticket_data: TicketTemp, number: int):
        question = []
        for tick in ticket_data.configure.ticket.category[number]:
            question.extend(ticket_data.question[tick])
        random.shuffle(question)
        count =  ticket_data.configure.ticket.count - len(question)
        if count > 0:
            question.extend((random.choice(question) for _ in range(count)))
        return question

    @classmethod
    def model_construct(cls, ticket_data: TicketTemp, _fields_set = None, **values):
        data: List[Dict[int, str]] = [{key: key for key in ticket_data.configure.ticket.category.keys()}
                                      for _ in range(ticket_data.configure.ticket.count)]
        question = {key: cls.question_to_list(ticket_data, key)
                    for key, _ in ticket_data.configure.ticket.category.items()}
        for key, _ in ticket_data.configure.ticket.category.items():
            for i, elem in enumerate(question[key]):
                data[i][key] = elem

        return cls(
            ticket_count=ticket_data.configure.ticket.count,
            questions=data,
            **ticket_data.configure.study
        )
