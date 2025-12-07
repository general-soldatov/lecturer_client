import json
import logging
from app.connect.gsheet import UserSheet
from app.connect.bucket import BucketManage

logger = logging.getLogger(__name__)

class BucketClient(BucketManage):
    def schedule(self, path='json', name='schedule.json'):
        """Функция конвертации расписания из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(self.config).shedule()
        self.json_upload(data, path, name)

    def contingent(self, path='json', name='contingent.json'):
        """Функция конвертации контингента из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(self.config).contingent(subject_bot=self.bucket_name)
        self.json_upload(data, path, name)
