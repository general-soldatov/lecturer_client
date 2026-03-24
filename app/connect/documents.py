import jinja2
from pydantic import BaseModel
from docxtpl import DocxTemplate
from xhtml2pdf import pisa, files
from htmldocx import HtmlToDocx
from docx import Document

class HtmlReader:
    def __init__(self, path_html, data: BaseModel):
        self.html_content = self.open_file(path_html)
        self.env = jinja2.Environment()
        self.data = data.model_dump()

    @staticmethod
    def open_file(path, encoding='utf-8'):
        with open(path, encoding=encoding) as file:
            return file.read()

    def render(self):
        template = self.env.from_string(self.html_content)
        self.html_content = template.render(**self.data)

    def create(self, path: str):
        pass


class HtmlToPDF(HtmlReader):
    def __init__(self, path_html: str, data: BaseModel):
        super().__init__(path_html, data)
        files.pisaFileObject.getNamedFile = lambda self: self.uri


    @staticmethod
    def _create(content, pdf_path, encoding='UTF-8'):
        with open(pdf_path, "w+b") as pdf_file:
            pisa_status = pisa.CreatePDF(content, dest=pdf_file, encoding=encoding)

        return not pisa_status.err

    def create(self, path: str):
        self.render()
        return self._create(self.html_content, path)

class HtmlToWord(HtmlReader):
    def __init__(self, path_html, data):
        super().__init__(path_html, data)
        self.parser = HtmlToDocx()
        self.doc = Document()

    def create(self, path: str):
        self.render()
        self.parser.add_styles_to_run('app/static/style_prot.css')
        self.parser.add_html_to_document(
            self.html_content, self.doc)
        self.parser.run_process()
        self.doc.save(path)


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
        return self._document_create(self.doc, self.name_file, self.data, self.jinja_env)


    @staticmethod
    def _document_create(docs: DocxTemplate, name_file: str, context: dict, jinja_env: jinja2.Environment) -> str | Exception:
        try:
            docs.render(context, jinja_env)
            docs.save(name_file)
            return name_file
        except Exception as e:
            return e