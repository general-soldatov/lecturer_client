from app.config.patent.yaml_config import ProjectReader
from app.documents.template_patent.word_template import AuthorConsentOne, AuthorConsentTwo, ReportOfPatent, DataOfAutors, ProgramTitle

def project(path: str, path_doc: str):
    project = ProjectReader(path)
    authorConsentOne = AuthorConsentOne(path_doc)
    authorConsentTwo = AuthorConsentTwo(path_doc)

    for i, _ in enumerate(project._data['info_authors'], 1):
        authorConsentOne.data = project.authorConsentOne(num_author=i)
        print(authorConsentOne.create_document())
        authorConsentTwo.data = project.authorConsentTwo(num_author=i)
        print(authorConsentTwo.create_document())

    report = ReportOfPatent(path_doc)
    report.data = project.reportOfPatent()
    print(report.create_document())

    authors = DataOfAutors(path_doc)
    authors.data = project.dataOfAutors()
    print(authors.create_document())

    program = ProgramTitle(path_doc)
    program.data = project.programTitle()
    print(program.create_document())