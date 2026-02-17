from app.config.patent.yaml_config import ProjectReader
from app.documents.template_patent.word_template import AuthorConsentOne, AuthorConsentTwo, ReportOfPatent, DataOfAutors, ProgramTitle

def project(path: str):
    project = ProjectReader(path)
    authorConsentOne = AuthorConsentOne()
    authorConsentTwo = AuthorConsentTwo()

    for i, _ in enumerate(project._data['info_authors'], 1):
        authorConsentOne.data = project.authorConsentOne(num_author=i)
        print(authorConsentOne.create_document())
        authorConsentTwo.data = project.authorConsentTwo(num_author=i)
        print(authorConsentTwo.create_document())

    report = ReportOfPatent()
    report.data = project.reportOfPatent()
    print(report.create_document())

    authors = DataOfAutors()
    authors.data = project.dataOfAutors()
    print(authors.create_document())

    program = ProgramTitle()
    program.data = project.programTitle()
    print(program.create_document())