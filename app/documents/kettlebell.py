import openpyxl
from typing import Literal, Tuple
import pandas as pd
from itertools import chain
from app.documents.word import KetllebellFlow, KetllebellSummary

PATH = "app/documents/template_kettlebell/protocol.xlsx"
CATEGORY = {
    'М': [63, 68, 73, 78, 85, 95],
    'Ж': [58, 63, 68]
}

EXCEL = {"step": {"М": 7, "Ж": 1}, "start": {"М": 3, "Ж": 52, "row": 14}, "command": 'B'}


class KettlebellCompetition:
    def __init__(self, path: str, boost: float = 2):
        self.path = path
        self.df: pd.DataFrame = None
        self.weight_category = {}
        self.set_weight_category()
        self.boost = boost
        self.offset_gender = {'М': 7, 'Ж': 1}


    @staticmethod
    def record(df: pd.DataFrame, path: str, sheet_name='results'):
        try:
            with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Record success")
        except Exception as e:
            print(e)

    @staticmethod
    def get_category(category: list, weight: float):
        for item in category:
            if item >= weight:
                return f"{item} кг"
        return f"{category[-1]}+ кг"

    def open_summary(self):
        self.df = pd.read_excel(self.path, sheet_name='results')
        self.count_members = len(self.df)
        self.count_commands = len(self.df['ВУЗ'].unique())

    def create_flow(self, first_members: Literal['М', 'Ж'], count_platform: int):
        self.df = pd.read_excel(self.path, sheet_name='register')
        self.assign_weight_category()
        self.df = self.sort_contest_weight(first_members)
        self.set_flow(count_platform)
        self.record(self.df, self.path)
        ketllebel = KetllebellFlow(self.df)
        ketllebel.create_document()

    def protocol(self, data: Tuple[Literal['М', 'Ж'], str]):
        df_1 = self.set_place(*data)
        summary = KetllebellSummary(df_1,
                                    members=self.count_members,
                                    commands=self.count_commands)
        summary.create_document(category=data)

    def create_protocol(self, gender: Literal['М', 'Ж'] | None = None, weight: str | None = None):
        self.open_summary()
        self.df['Год рождения'] = self.df['Год рождения'].dt.strftime('%d.%m.%Y')
        self.df.loc[self.df['Разряд'].isna(), 'Разряд'] = '-'
        if gender and weight:
            return self.protocol((gender, weight))
        for gender, weights in self.weight_category.items():
            for weight in weights:
                self.protocol((gender, weight))

    def set_weight_category(self):
        for key, value in CATEGORY.items():
            self.weight_category[key] = []
            for item in value:
                self.weight_category[key].append(
                    self.get_category(value, item))
            self.weight_category[key].append(
                    self.get_category(value, value[-1] + 1))

    def assign_weight_category(self, weight_column='Вес, кг',
                            gender_column='Пол'):
        self.df['В/К'] = self.df.apply(
            lambda row: self.get_category(CATEGORY[row[gender_column]], row[weight_column]),
            axis=1
        )

    def sort_contest_weight(self, first_members: Literal['М', 'Ж'],
                            column_weight_category='В/К', column_group='Группа',
                            column_draw_nuber='Жеребьёвка', gender_column='Пол'):
        df_copy = self.df.copy()
        df_copy['weight_kg'] = df_copy[column_weight_category].replace({r'(\+)': '5'},
                                                                       regex=True).str.extract(r'(\d+)').astype(float)
        df_copy.loc[df_copy[column_group].isna(), column_group] = 'Б'
        df_copy = df_copy.sort_values(
            by=[gender_column, 'weight_kg', column_group, column_draw_nuber],
            ascending=[(first_members == 'Ж'), True, False, True]
        ).drop('weight_kg', axis=1).reset_index(drop=True)
        return df_copy

    def set_flow(self, count_platform: int, column_flow='Поток', column_platform='Помост'):
        count_of_members = len(self.df)
        self.df[column_flow] = [((i // count_platform) + 1) for i in range(count_of_members)]
        self.df[column_platform] = [((i % count_platform) + 1) for i in range(count_of_members)]
        self.df['Результат'] = pd.NA

    @staticmethod
    def place_sportsman(count_sportsman, min_score = 0.25):
        sequence = [20, 18, 16, *range(15, 1, -1), 0.5]
        count_sequence = len(sequence)
        if count_sportsman <= count_sequence:
            return sequence[:count_sportsman]
        return list(chain(sequence,
                        [min_score] * (count_sportsman - count_sequence)))

    @staticmethod
    def calculate_score(score: int, gender: Literal['М', 'Ж'], kettlebel: int, boost: float):
        boost_data = {'М': 32, 'Ж': 24}
        if kettlebel == boost_data[gender]:
            return score * boost
        return score

    def set_place(self, gender: Literal['М', 'Ж'], weight_category: str):
        df1 = self.df.copy()
        df1 = df1.loc[(df1['В/К'] == weight_category) & (df1['Пол'] == gender)]
        df1['score'] = df1.apply(
            lambda row: self.calculate_score(row['Результат'],
                                             gender, row['Гиря'], self.boost),
            axis=1
        )
        df1 = df1.sort_values(by=['score', 'Вес, кг', 'Жеребьёвка'], ascending=[False, True, True])
        count_sportsman = len(df1)
        df1['place'] = list(range(1, count_sportsman + 1))
        df1['score_command'] = self.place_sportsman(count_sportsman)
        return df1

    def set_place_all(self) -> pd.DataFrame:
        lst = []
        for gender, value in self.weight_category.items():
            for weight in value:
                df_1 = self.set_place(gender, weight)
                lst.append(df_1)
        return pd.concat(lst, axis=0)

    @staticmethod
    def weight_to_dict(df: pd.DataFrame):
        data = df.to_dict('list')
        result = {"total": 0}
        for id, score in enumerate(data['score_command']):
            result.setdefault(data['В/К'][id], [])
            result[data['В/К'][id]].append(score)
            result['total'] += score
        return result

    def get_commands(self):
        commands = {}
        offset = lambda df, gender: self.weight_to_dict(df[df['Пол'] == gender][
            ['В/К', 'place', 'score_command']].sort_values(['place'],
        ascending=[True]).head(self.offset_gender[gender]))

        for item in self.set_place_all().groupby(['ВУЗ']):
            commands[item[0][0]] = {key: offset(item[1], key)
                                    for key in self.offset_gender}
            commands[item[0][0]]['total_score'] = commands[item[0][0]]['М']['total'] + commands[item[0][0]]['Ж']['total']

        return sorted(commands.items(), key=lambda x: x[1]['total_score'], reverse=True)

    def create_commands_protocol(self, path: str):
        self.open_summary()
        wb = openpyxl.load_workbook(PATH, read_only=False)
        sheet = wb['summary']
        sheet['C9'] = self.count_commands
        sheet['C10'] = self.count_members
        for place, command in enumerate(self.get_commands(), 1):
            row = EXCEL['start']['row'] + place - 1
            sheet[f"A{row}"] = place
            sheet[f"B{row}"] = command[0]
            sheet[f"BD{row}"] = command[1]['total_score']
            for gender, category in self.weight_category.items():
                for i, elem in enumerate(category):
                    col = EXCEL['start'][gender] + EXCEL['step'][gender] * i
                    for score in command[1][gender].get(elem, []):
                        sheet.cell(row, col, score)
                        col += 1

        wb.save(path)