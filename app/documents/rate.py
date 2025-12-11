import jinja2
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict
from app.connect.documents import HtmlToPDF
from app.connect.bucket import BucketManage
from app.config.configure import YamlProject

class Statement(BaseModel):
    discipline: str
    learn_year: str
    faculty: str
    direct: str
    name: List[str]
    score: List[int | float]
    rate: List[int]
    stars: List[int]
    ticket: str = " "

class Summary(YamlProject):
    discipline: str
    learn_year: str
    faculty: str
    directs: Dict[str, str]
    course: int
    export_folder: str
    name_document: str


class StatementOfSemestr(HtmlToPDF):
    def __init__(self, path_html: str, data: Statement):
        super().__init__(path_html)
        self.environment = jinja2.Environment()
        self.data = data.model_dump()

    def render(self):
        template = self.environment.from_string(self.html_content)
        self.html_content = template.render(**self.data)

class DownloadClient(BucketManage):
    def __init__(self, bucket_name, config, session_aws = None):
        super().__init__(bucket_name, config, session_aws)
        self.contingent: pd.DataFrame = None
        self.list_profile: list = None
        self.rate: pd.DataFrame = None

    def _get_contingent(self, folder='json', name='contingent.json') -> dict:
        return self.json_download(folder, name)

    def _get_rate(self, filename, folder='rate'):
        return super().json_download(folder, filename)

    def _get_list_of_students(self):
        contingent = [{'name': key, **value}
                      for key, value in self._get_contingent().items()]
        self.contingent = pd.json_normalize(contingent)
        # self.list_profile = self.contingent['profile'].unique()

    def _get_rates_of_study(self):
        return [elem for profile in self.list_profile
                for elem in self._get_rate(f"{profile}.json")]

    @staticmethod
    def get_fine(score):
        star = {5: 60, 4: 50, 3: 40, 2: 25, 1: 10}
        for key, value in star.items():
            if float(score['score']) > value:
                return key
        return 0

class RateCreator(DownloadClient):
    def __init__(self, bucket_name, config, path_yaml, session_aws=None, html_path='app/static/index.html'):
        super().__init__(bucket_name, config, session_aws)
        self.html_path = html_path
        self.project = Summary.model_validate_yaml(path_yaml)
        self.list_profile = self.project.directs.keys()

    def merge_contingent(self):
        self._get_list_of_students()
        df = pd.json_normalize(self._get_rates_of_study())
        self.contingent = pd.merge(self.contingent[['name', 'group']],
                                   df, on='name')
        self.contingent['stars'] = self.contingent.apply(self.get_fine, axis=1)

    def _contingent_to_dict(self, profile):
        return self.contingent[self.contingent['profile'] == profile].to_dict(orient='list')

    @staticmethod
    def loger(info, path):
        if info:
            print(f'File create at path {path}')
        else:
            print(f'Error: {info}')

    def create_pdf(self):
        self.merge_contingent()
        for profile in self.list_profile:
            state = Statement(
                learn_year=self.project.learn_year,
                faculty=self.project.faculty,
                discipline=self.project.discipline,
                direct=self.project.directs[profile],
                **self._contingent_to_dict(profile)
            )
            document = StatementOfSemestr(self.html_path, state)
            pdf_path = self.path_name(
                self.project.export_folder,
                f"{self.project.name_document}_{self.project.discipline}_{profile}.pdf")
            info = document.create_pdf(pdf_path)
            self.loger(info, pdf_path)
