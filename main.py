import logging
import click
import shutil
import json
from app.config.configure import Configure
from app.config.tickets import TicketTemp, TicketOutput
from app.connect.bucket import BucketClient
from app.connect.db import load_contingent, order, UserVar
from app.documents.word import WordTicket, WordQuestion
from app.documents.rate import RateCreator
from app.documents.patent import project


@click.group()
def cli():
    pass

logging.basicConfig(
    level=logging.INFO,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)
logger = logging.getLogger(__name__)

def logger_set(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
    return inner

PATH = 'C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/config/setting.yaml'
config: Configure = Configure.model_validate_yaml(PATH)

@cli.command("create", help="Create template of makefile")
@click.option("--type", prompt="Type of file", type=click.Choice(["patent", "ticket"]))
@click.option("--name", prompt="Name of file")
@logger_set
def create(type: str, name: str):
    data = {
        "patent": "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_make/patent.yaml",
        "ticket": "C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/app/documents/template_make/phys_biotech.yaml"
    }
    name += ".yaml"
    shutil.copy(data[type], name)
    click.echo(f"File {type}: {name} create successful!")

@cli.command("upload", help="Upload schedule or contingent to bucket")
@click.option("--doc", "-d", prompt="Document", type=click.Choice(["schedule", "contingent"]))
@click.option("--subject", prompt="Subject", type=click.Choice(["termex", "physics"]))
@logger_set
def upload(doc: str, subject: str):
    """
    Docstring для load_shedule
    This function is loading shedule at json-format to termex-bucket or loading contingent at json-format to bucket

    :param doc: Type of document to load
    :type doc: str
    :param discipline: Name of discipline as physics or termex
    :type discipline: str
    """
    if doc == "schedule":
        name = config.discipline['termex']
        s3 = BucketClient(name.bucket_name, config=config)
        s3.schedule()
    elif doc == "contingent":
        s3 = BucketClient(
        config.discipline[subject].bucket_name, config=config)
        s3.contingent()

@cli.command("learn", help="Build learn's documents from makefiles")
@click.option("--types", prompt="Type", type=click.Choice(["tickets", "questions", "summary"]))
@click.option("--path", prompt="Path", help="Check path to makefile")
@click.option("--subject", prompt="Subject", type=click.Choice(["termex", "physics"]))
@logger_set
def create_tickets(types: str, path: str, subject: str):
    """
    Docstring для create_tickets

    :param path: Path to yaml-project
    :type path: str
    """
    match types:
        case "summary":
            data = RateCreator(
            config.discipline[subject].bucket_name, config=config,
            path_yaml=path)
            data.create_pdf()
        case "tickets":
            ticket_data = TicketTemp.model_validate_yaml(path)
            tickets = TicketOutput.model_construct(ticket_data)
            word = WordTicket(tickets, path_folder="export")
            word.create_document()
        case "questions":
            ticket_data = TicketTemp.model_validate_yaml(path)
            word = WordQuestion(ticket_data, path_folder="export")
            word.create_document()

@cli.command("patent", help="Build documents from makefiles")
@click.option("--path", prompt="Path", help="Check path to makefile")
@click.option("--folder", prompt="Folder", help="Check folder to output", default="export")
@logger_set
def patent(path: str, folder: str):
    project(path, folder)

@cli.command("download", help="Download contingent from database")
@click.option("--subject", prompt="Subject", type=click.Choice(["termex", "phys"]))
@click.option("--year", prompt="Year of learning")
@logger_set
def download(subject: str, year: str):
    load_contingent(subject, year)

@cli.command("clean_up", help="Clean up of contingent")
@click.option("--subject", prompt="Subject", type=click.Choice(["termex", "phys"]))
@click.option("--path", prompt="Path to contingent")
@logger_set
def clean_up(subject: str, path: str):
    data = order(subject, path)
    uv = UserVar(subject)
    for item in data:
        if click.confirm(f"Are you want delete from database user {item['name']}", default=True):
            res = uv.delete_note(int(item['user_id']))
            click.echo(f"User {item['name']} was deleted!")
            print('Data:', res)


# import requests
# response = requests.get('https://storage.yandexcloud.net/termex-bot/json/contingent.json')
# print(response.json()['Ковальчук Фёдор Сергеевич'])
if __name__ == '__main__':
    cli()