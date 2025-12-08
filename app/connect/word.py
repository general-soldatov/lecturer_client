import jinja2
from docxtpl import DocxTemplate
from app.config.tickets import TicketOutput

class WordDocument:
    def __init__(self, path_doc: str = None, path: str = ""):
        self.doc: DocxTemplate = DocxTemplate(path)
        self.data: dict = {'full_name': "NoName"}
        self.type_doc: str = "NoneType"
        self.name_file = ""
        self.path_doc = path_doc
        self.jinja_env = jinja2.Environment()

    def create_name(self):
        path = self.path_doc + "/" if self.path_doc else ""
        self.name_file = f"{path}{self.type_doc.upper()}_{self.data['faculty'].capitalize()}_{self.data['direct']}.docx"

    def create_document(self) -> str | Exception:
        self.create_name()
        return self.__document_create(self.doc, self.name_file, self.data, self.jinja_env)


    @staticmethod
    def __document_create(docs: DocxTemplate, name_file: str, context: dict, jinja_env: jinja2.Environment) -> str | Exception:
        try:
            docs.render(context, jinja_env)
            docs.save(name_file)
            return name_file
        except Exception as e:
            return e

class WordTicket(WordDocument):
    def __init__(self, tickets: TicketOutput, path_doc = None, path = "app/config/ticket.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Билеты"
        self.data = tickets.model_dump()
        # self.data['faculty'] = self.data['faculty'].upper()
