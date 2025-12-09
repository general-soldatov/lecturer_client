import boto3
import logging
import json

import boto3.session
from app.connect.gsheet import UserSheet
from app.config.configure import AWSSession, AWSConfig, Configure, Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BucketManage:
    def __init__(self, bucket_name: str, config: AWSConfig | dict | Configure, session_aws: AWSSession | dict = None):
        if isinstance(config, AWSConfig):
            configure = config.__dict__
        if isinstance(session_aws, AWSSession):
            session_aws = session_aws.__dict__
        if isinstance(config, Configure):
            session_aws = Session.model_construct(config.aws).model_dump()
            configure = AWSConfig.model_construct_s3(config).model_dump()
            self.config = config
        self.s3 = boto3.session.Session(**session_aws).resource(**configure)
        self.bucket_name = bucket_name
        self.temp_path = 'app/temp'

    def json_upload(self, data: dict, path=None, name='name.json'):
        schedule = json.dumps(data, ensure_ascii=False, indent=4)
        path_bucket = f'{path}/{name}' if path else name
        self.s3.Object(self.bucket_name, path_bucket).put(Body=schedule)
        logger.error(f'File {name} upload to bucket {self.bucket_name}')

    def json_download(self, name):
        pass



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
