import logging
import requests
# from app.function import schedule_json
from app.config.configure import bucket_config, AWSSession
from app.connect.bucket import BucketManage
from app.function import BucketClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# BucketManage(bucket_name='termex-bot').schedule()
BucketClient().contingent(bucket='phys-bot')


response = requests.get('https://storage.yandexcloud.net/phys-bot/json/contingent.json')
print(response.json())