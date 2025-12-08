import logging
from app.config.configure import Configure
from app.config.tickets import TicketTemp, TicketOutput
from app.connect.bucket import BucketClient
from app.connect.word import WordTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PATH = 'app/config/setting.yaml'
config: Configure = Configure.model_validate_yaml(PATH)

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
    # print(tickets)
    word = WordTicket(tickets)
    word.create_document()

# load_contingent(discipline='physics')
# load_contingent(discipline='termex')
# load_shedule()
create_tickets(path='projects/phys_process_animal.yaml')


# response = requests.get('https://storage.yandexcloud.net/phys-bot/json/contingent.json')
# print(response.json()['Девятаева Виктория Романовна'])
