import jinja2
from docxtpl import DocxTemplate

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
        self.name_file = f"{path}{self.type_doc}_{self.data['full_name']}.docx"

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

class AuthorConsentOne(WordDocument):
    def __init__(self, path_doc = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_patent/authors_consent_1.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Согласие_п.3"
        self.data = {}


class AuthorConsentTwo(WordDocument):
    def __init__(self, path_doc = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_patent/authors_consent_2.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Согласие_п.4"
        self.data = {}


class ReportOfPatent(WordDocument):
    def __init__(self, path_doc = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_patent/report_template.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Реферат"
        self.data = {}


class DataOfAutors(WordDocument):
    def __init__(self, path_doc = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_patent/data_of_authors.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Сведения_авторы"
        self.data = {}

class ProgramTitle(WordDocument):
    def __init__(self, path_doc = None, path = "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_patent/program_title.docx"):
        super().__init__(path_doc, path)
        self.type_doc = "Листинг_программы"
        self.data = {}


if __name__ == "__main__":
    output_file = DataOfAutors().create_document()
    print(f"Document create {output_file}")