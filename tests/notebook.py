import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client')))

from docx import Document
from app.documents.test import LabGenerator
from app.documents.test_make import Project
from docx.shared import Inches, Pt, Cm




# project = Project.open_project("projects/termex_notebook.yaml")
# build_labs(project, )
PATH = os.path.join("projects", "termex")
NAME = 'notebook_termex.docx'
IMAGE_FOLDER_NAME = "images_task"
def notebook(path, name, image):
    image = os.path.join(path, image)
    list_of_projects = [f for f in os.listdir(path) if f.endswith('.yaml')]
    doc = Document()
    for section in doc.sections:
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1)
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
    style = doc.styles['Normal']
    # название шрифта по умолчанию
    style.font.name = 'Times New Roman'
    # размер шрифта по умолчанию
    style.font.size = Pt(11)
    for i, elem in enumerate(list_of_projects, 1):
        project = Project.model_validate_yaml(os.path.join(path, elem))
        lab = LabGenerator(i, project, image, doc = doc)
        lab.generate_labs()

    doc.save(os.path.join(path, name))
    print("\n✨ Проект успешно создан! Откройте файл:", os.path.join(path, name))

notebook(PATH, NAME, IMAGE_FOLDER_NAME)