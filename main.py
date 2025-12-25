import logging
from app.config.configure import Configure
from app.config.tickets import TicketTemp, TicketOutput
from app.connect.bucket import BucketClient
from app.documents.word import WordTicket, WordQuestion
from app.documents.rate import RateCreator

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

PATH = 'app/config/setting.yaml'
config: Configure = Configure.model_validate_yaml(PATH)

@logger_set
def load_shedule():
    """
    Docstring для load_shedule
    This function is loading shedule at json-format to termex-bucket
    """
    name = config.discipline['termex']
    s3 = BucketClient(name.bucket_name, config=config)
    s3.schedule()

def load_contingent(discipline: str):
    """
    Docstring для load_contingent
    This function is loading contingent at json-format to bucket

    :param discipline: Name of discipline as physics or termex
    :type discipline: str
    """
    s3 = BucketClient(
        config.discipline[discipline].bucket_name, config=config)
    s3.contingent()

def create_tickets(path: str):
    """
    Docstring для create_tickets

    :param path: Path to yaml-project
    :type path: str
    """
    ticket_data = TicketTemp.model_validate_yaml(path)
    tickets = TicketOutput.model_construct(ticket_data)
    word = WordTicket(tickets, path_folder="export")
    word.create_document()

@logger_set
def create_questions(path: str):
    ticket_data = TicketTemp.model_validate_yaml(path)
    word = WordQuestion(ticket_data, path_folder="export")
    word.create_document()

@logger_set
def create_summary(discipline):
    data = RateCreator(
        config.discipline[discipline].bucket_name, config=config,
        path_yaml="projects/summary.yaml")
    data.create_pdf()

# load_contingent(discipline='physics')
# load_contingent(discipline='termex')
# load_shedule()
# PATH = "projects/phys_spo.yaml"
# create_tickets(PATH)
# create_questions(PATH)
# create_summary(discipline='physics')
from app.connect.elib import *
# response = requests.get('https://storage.yandexcloud.net/phys-bot/json/contingent.json')
# print(response.json()['Девятаева Виктория Романовна'])
