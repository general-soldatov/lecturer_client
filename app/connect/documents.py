import jinja2
from docxtpl import DocxTemplate
from xhtml2pdf import pisa, files

class HtmlToPDF:
    def __init__(self, path_html):
        self.html_content = self.open_file(path_html)
        files.pisaFileObject.getNamedFile = lambda self: self.uri

    @staticmethod
    def open_file(path, encoding='utf-8'):
        with open(path, encoding=encoding) as file:
            return file.read()

    @staticmethod
    def _create(content, pdf_path, encoding='UTF-8'):
        with open(pdf_path, "w+b") as pdf_file:
            pisa_status = pisa.CreatePDF(content, dest=pdf_file, encoding=encoding)

        return not pisa_status.err

    def render(self):
        pass

    def create_pdf(self, path):
        self.render()
        return self._create(self.html_content, path)


class WordDocument:
    def __init__(self, path_folder: str = None, path: str = ""):
        self.doc: DocxTemplate = DocxTemplate(path)
        self.data: dict = {'full_name': "NoName"}
        self.type_doc: str = "NoneType"
        self.name_file = ""
        self.path_doc = path_folder
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