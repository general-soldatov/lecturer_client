import json
import logging
from app.connect.gsheet import UserSheet
from app.connect.bucket import BucketManage

logger = logging.getLogger(__name__)

class BucketClient:
    def __init__(self):
        pass

    def schedule(self, path='json', name='schedule.json'):
        """Функция конвертации расписания из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(user_id='333').shedule()
        BucketManage('termex-bot').json_upload(data, path, name)

    def contingent(self, path='json', name='contingent.json', bucket='termex-bot'):
        """Функция конвертации контингента из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(user_id='33').contingent(subject_bot=bucket)
        BucketManage(bucket).json_upload(data, path, name)
