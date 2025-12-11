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