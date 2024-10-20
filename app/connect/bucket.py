import boto3
import logging
import json
import os

import boto3.session
from app.config.configure import AWSSession, AWSConfig, bucket_config
from app.connect.gsheet import UserSheet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BucketManage:
    def __init__(self, bucket_name: str, config: AWSConfig | dict = bucket_config, session_aws: AWSSession | dict = AWSSession()):
        if isinstance(config, AWSConfig):
            config = config.__dict__
        if isinstance(session_aws, AWSSession):
            session_aws = session_aws.__dict__
        self.s3 = boto3.session.Session(**session_aws).resource(**config)
        self.bucket_name = bucket_name
        self.temp_path = 'app/temp'

    def json_upload(self, data: dict, path=None, name='name.json'):
        schedule = json.dumps(data, ensure_ascii=False, indent=4)
        path_bucket = f'{path}/{name}' if path else name
        self.s3.Object(self.bucket_name, path_bucket).put(Body=schedule)
        logger.error(f'File {name} upload to bucket {self.bucket_name}')
