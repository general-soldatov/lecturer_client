import gspread
from datetime import datetime
from gspread import exceptions
from time import sleep
from progress.bar import IncrementalBar

from app.config.configure import DBConfig


class UserSheet:
    def __init__(self, user_id, table="Термех 2/2024"):
        self.user_id = user_id
        self.gs = gspread.service_account(filename=DBConfig.google_api)
        self.table = self.gs.open(table)
        self.rate = self.table.worksheet('rate')
        self.task_head = {
            'S1': 'E', 'S2': 'F', 'S3': 'G', 'S4': 'H', 'S5': 'I', 'S6': 'J',
            'K1': 'K', 'K2': 'L', 'K3': 'M', 'K4': 'N', 'K5': 'O',
            'D1': 'P', 'D2': 'Q', 'D3': 'R', 'D4': 'S', 'D5': 'T', 'D6': 'U'
            }

    def user_search(self, name):
        contingent = self.table.worksheet('contingent')
        all_rows = contingent.get_all_values()
        lst = []
        for row in all_rows:
            if len(name) <= 0:
                break
            if row[0].lower() == name.lower():
                lst = row
                return {
                    'user_id': self.user_id,
                    'name': lst[0],
                    'profile': lst[1],
                    'group': f'{lst[2]}-{lst[3]}',
                    'date': str(datetime.now()),
                    'var': lst[4],
                    'varD': lst[5]
                }
        return False

    def contingent(self):
        contingent = self.table.worksheet('contingent')
        all_rows = contingent.get_all_values()
        data = {}
        for i, row in enumerate(all_rows[1:], 1):
            data[row[0]] = {
                    'google_id': str(i),
                    'profile': row[1],
                    'group': f'{row[2]}-{row[3]}',
                    'var': row[4],
                    'varD': row[5]
                }

        return data

    def user_info(self, google_id):
        header = self.rate.row_values(1)
        info = self.rate.row_values(google_id)
        return {key: value for key, value in zip(header, info)}

    def add_task(self, google_id, task, ball):
        word = self.task_head[task]
        self.rate.update_acell(f'{word}{google_id}', ball)
        return 'ok'

    def shedule(self):
        shedule = self.table.worksheet('shedule')
        lst = shedule.get_all_values()

        days = lst[0][1:]
        schedule = lst[1:]
        data = {
            '0': {},
            '1': {}
        }

        for day in days:
            data['0'][day] = {}
            data['1'][day] = {}

        for i, tms in enumerate(schedule, 1):
            for j, disc in enumerate(tms[1:]):
                if disc == '':
                    continue
                data[str(i%2)][days[j]].update({tms[0]: disc.replace('\n', ' ').replace('  ', ' ')})

        return data


    def create_contingent(self, lst_name):
        lst = self.table.worksheet('contingent')
        set_header = ['name', 'profile', 'lection_non', 'seminar',
                       *self.task_head.keys(), 'task_bot', 'gift',
                       'lab', 'sum', 'summary', 'rate', 'score']
        try:
            contingent = self.table.worksheet(lst_name)
        except exceptions.WorksheetNotFound:
            contingent = self.table.add_worksheet(title=lst_name, rows="100", cols="30")
        contingent.insert_row(set_header)
        rows = lst.get_all_records()[1:]
        bar = IncrementalBar('GSheet Record', max=len(rows))
        for i, row in enumerate(rows, 2):
            contingent.update_acell(f'A{i}', row['name'])
            contingent.update_acell(f'B{i}', row['profile'])
            bar.next()
            sleep(1)
            contingent.update_acell(f'X{i}', f'=СУММ(D{i}:V{i})')
            contingent.update_acell(f'Y{i}', f'=X{i}-C{i}')
            contingent.update_acell(f'Z{i}', f'=Y{i}*(W{i}+1)')
            sleep(2)

        bar.finish()
        return 'ok'