import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client')))

from app.documents.test import LabGenerator, build_labs
from app.documents.test_make import Project

project = Project.open_project("projects/termex_notebook.yaml")
build_labs(project, 'notebook.docx')
