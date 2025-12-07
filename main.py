import logging
import requests
# from app.function import schedule_json
from app.config.configure import Configure
from app.function import BucketClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PATH = 'app/config/setting.yaml'
config: Configure = Configure.model_validate_yaml(PATH)
DISCIPLINE = config.discipline['termex']
# DISCIPLINE = config.discipline['physics']
s3 = BucketClient(DISCIPLINE.bucket_name, config=config)

# Upload of the contingent
# s3.contingent()
# Upload of the lecture's shedule
# s3.schedule()

# response = requests.get('https://storage.yandexcloud.net/phys-bot/json/contingent.json')
# print(response.json()['Девятаева Виктория Романовна'])
