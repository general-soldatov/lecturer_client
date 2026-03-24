from pandas import DataFrame
from app.config.tickets import TicketOutput, TicketTemp
from app.connect.documents import WordDocument


class WordTicket(WordDocument):
    def __init__(self, tickets: TicketOutput, path_folder = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/config/configure.py"):
        super().__init__(path_folder, path)
        self.type_doc = "Билеты"
        self.data = tickets.model_dump()

class WordQuestion(WordDocument):
    def __init__(self, tickets: TicketTemp, path_folder = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/config/questions.docx"):
        super().__init__(path_folder, path)
        self.type_doc = "Вопросы"
        self.data = {
            'questions': tickets.export_question(),
            **tickets.configure.study
        }

class KetllebellFlow(WordDocument):
    def __init__(self, df: DataFrame, path_folder = None, path = "app/documents/template_kettlebell/flows.docx"):
        super().__init__(path_folder, path)
        self.type_doc = "Потоки_Вузы"
        self.data = {"data": {key: value.to_dict(orient='records') for key, value in df.groupby(by='Поток')}}

    def create_name(self):
        path = self.path_doc + "/" if self.path_doc else ""
        self.name_file = f"{path}{self.type_doc}.docx"

class KetllebellSummary(WordDocument):
    def __init__(self, df: DataFrame, path_folder = None, path = "app/documents/template_kettlebell/summary.docx", **kwargs):
        super().__init__(path_folder, path)
        self.type_doc = "Результаты_Вузы"
        self.df = {key: value.to_dict(orient='records') for key, value in df.groupby(by=['Пол', 'В/К'])}
        self.data = {"exercise": {'М': 'Толчок', 'Ж': 'Рывок'}, "gender": {'М': 'Мужчины', 'Ж': 'Женщины'}}
        self.data.update(kwargs)

    def create_name(self, gender, weight_category):
        path = self.path_doc + "/" if self.path_doc else ""
        self.name_file = f"{path}{self.type_doc}_{gender}_{weight_category}.docx"

    def create_document(self, category: tuple = None) -> str | Exception:
        if category:
            self.create_name(*category)
            self.data.update({"data": self.df[category], "category": category})
            return print(self._document_create(self.doc, self.name_file, self.data, self.jinja_env))
        for key, value in self.df.items():
            self.create_name(*key)
            self.data = {"data": value, "category": key}
            print(self._document_create(self.doc, self.name_file, self.data, self.jinja_env))
