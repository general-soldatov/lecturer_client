from xhtml2pdf import pisa, files
import jinja2
from pydantic import BaseModel
from typing import List

class Statement(BaseModel):
    learn_year: str
    faculty: str
    direct: str
    name_data: List[str]
    score_data: List[int]
    rate_data: List[int]
    stars_data: List[int]
    ticket: str = " "

class HtmlToPDF:
    def __init__(self, path_html):
        self.html_content = self.open_html(path_html)

    @staticmethod
    def open_html(path, encoding='utf-8'):
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

class StatementOfSemestr(HtmlToPDF):
    def __init__(self, path_html: str, data: Statement):
        super().__init__(path_html)
        self.environment = jinja2.Environment()
        self.data = data.model_dump()

    def render(self):
        template = self.environment.from_string(self.html_content)
        self.html_content = template.render(**self.data)



# PDF path to save
pisa.showLogging()
html_path = 'index.html'
pdf_path = "google.pdf"

state = Statement(
    learn_year='2025/2026',
    faculty='Tech',
    direct='Biotech',
    name_data=['Yura Igorevich Soldatov', 'Elvira Viktorovna Soldatova-Mal\'ugina'],
    score_data=[22, 22],
    rate_data=[1, 1],
    stars_data=[5, 5]
)

files.pisaFileObject.getNamedFile = lambda self: self.uri
document = StatementOfSemestr(html_path, state)
document.create_pdf(pdf_path)

# Generate PDF
# pdf = HtmlToPDF(html_path)
# if pdf.create_pdf(pdf_path):
#     print(f"PDF generated and saved at {pdf_path}")
# else:
#     print("PDF generation failed")