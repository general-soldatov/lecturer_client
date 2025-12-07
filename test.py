import re
from app.connect.gsheet import UserSheet
from datetime import datetime
from openpyxl import Workbook, load_workbook
from app.config.configure import Session, Configure, TicketTemp
from pydantic import BaseModel, Field
from typing import Dict, List

PATH = 'app/config/setting.yaml'
config = Configure.model_validate_yaml(PATH)
session = Session.model_construct(config.aws)

file_name = 'contingent.xlsx'
# data = UserSheet(config)

delimiter = datetime(2025, 1, 1).isocalendar()[1]
delimiter %= 2

class Lesson(BaseModel):
    time: str
    data: str

class LessonOfWeek(BaseModel):
    second: Dict[str, List[Lesson]] = Field(alias='0')
    first: Dict[str, List[Lesson]] = Field(alias='1')

    @staticmethod
    def reconstruct_model(data: Dict[str, Dict[str, Dict[str, str]]]):
        obj = {}
        for week, days in data.items():
            obj.setdefault(week, {})
            for day, shed in days.items():
                obj[week].setdefault(day, [])
                obj[week][day] = [{'time': times, 'data': lesson} for times, lesson in shed.items()]
        return obj

    @classmethod
    def model_construct(cls, data: Dict[str, Dict[str, Dict[str, str]]], _fields_set = None, **values):
        obj = cls.reconstruct_model(data)
        return cls.model_validate(obj)

# schedule = data.shedule()
# contingent = data.contingent(subject_bot='phys-bot')
# schedule = {'0': {'ПОНЕДЕЛЬНИК': {'11.40-13.15': 'Физика, Тбиотех1-4 лекц. 243 г.к.'}, 'ВТОРНИК': {'15.50-17.25': 'Физика, ТППРС-1-5б лаб. 247 г.к.', '17.40-19.15': 'Физика, ТППРС-1-5б лаб. 247 г.к.'}, 'СРЕДА': {'11.40-13.15': 'Физика, ТППЖП-1-6 лаб. 244 г.к.', '14.00-15.35': 'Физика, ТППЖП-1-6 лаб. 244 г.к.'}, 'ЧЕТВЕРГ': {'9.50-11.25': 'Физика, Тжир1 лекц. 246 г.к.', '11.40-13.15': 'Физика, Тбиотех1-4а лаб. 244 г.к.', '14.00-15.35': 'Физика, Тбиотех1-4а лаб. 244 г.к.'}, 'ПЯТНИЦА': {'8.00-9.35': 'Физика, ТППРС-1-5а лаб. 244 г.к.', '9.50-11.25': 'Физика, ТППРС-1-5а лаб. 244 г.к.', '11.40-13.15': 'Физика, Тбиотех1-4б лаб. 243 г.к.', '14.00-15.35': 'Физика, Тбиотех1-4б лаб. 243 г.к.'}, 'СУББОТА': {}, 'ВОСКРЕСЕНЬЕ': {}}, '1': {'ПОНЕДЕЛЬНИК': {'11.40-13.15': 'Физика, Тбиотех1-4 лекц. 243 г.к.'}, 'ВТОРНИК': {'8.00-9.35': 'Физика, ТППРС-1-5б лаб. 247 г.к.', '9.50-11.25': 'Физика, ТППРС-1-5б лаб. 247 г.к.', '11.40-13.15': 'Кураторский час'}, 'СРЕДА': {'11.40-13.15': 'Физика, ТППЖП-1-6 лаб. 244 г.к.', '14.00-15.35': 'Физика, ТППЖП-1-6 лаб. 244 г.к.'}, 'ЧЕТВЕРГ': {'9.50-11.25': 'Физика, Тжир1 лекц. 246 г.к.', '11.40-13.15': 'Физика, Тбиотех1-4а лаб. 244 г.к.', '14.00-15.35': 'Физика, Тбиотех1-4а лаб. 244 г.к.'}, 'ПЯТНИЦА': {'8.00-9.35': 'Физика, ТППРС-1-5а лаб. 244 г.к.', '9.50-11.25': 'Физика, ТППРС-1-5а лаб. 244 г.к.', '11.40-13.15': 'Физика, Тбиотех1-4б лаб. 243 г.к.', '14.00-15.35': 'Физика, Тбиотех1-4б лаб. 243 г.к.'}, 'СУББОТА': {}, 'ВОСКРЕСЕНЬЕ': {}}}
# data = LessonOfWeek.model_construct(schedule)
# print(schedule[str(delimiter)])
# print(data)
PROJECT = 'projects/phys.yaml'
ticket_data = TicketTemp.model_validate_yaml(PROJECT)
print(ticket_data)

class TicketOutput(BaseModel):
    year: str
    discipline: str
    first: List[str]
    second: List[str]
    third: List[str]
# wb = load_workbook(file_name)

# ws = wb['Example']

# groups = {}
# for name, value in contingent.items():
#     groups.setdefault(f"{value['profile']}-{value['group']}", [])
#     groups[f"{value['profile']}-{value['group']}"].append(name)

# for group, names in groups.items():
#     target = wb.copy_worksheet(ws)
#     target.title = group
#     for i, name in enumerate(names, 3):
#         target[f'A{i}'] = name


# wb.save(file_name)


# labs = {}

# for day, times in schedule[str(delimiter)].items():
#     for time, subject in times.items():
#         if 'лаб.' in subject:
#             group = subject.split(',')[1].strip().split(' лаб. ')[0]
#             if group not in labs:
#                 labs[group] = []
#             labs[group].append(day)

# for group, sessions in labs.items():
#     print(f"Группа: {group}")
#     for session in sessions:
#         print(f"  - {session}")

# dat = re.split(r'^(\w+)\s\d{2}\.\d{2}-\d{2}\.\d{2}$', "СРЕДА 11.40-13.15")
# print(dat)
# print('success')
# # print(chr(col))