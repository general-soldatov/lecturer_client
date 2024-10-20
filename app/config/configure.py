from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

load_dotenv()

@dataclass
class AWSSession:
    region_name: str = getenv('AWS_DEFAULT_REGION')
    aws_access_key_id: str = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class AWSConfig:
    service_name: str
    endpoint_url: str


google_api: str = getenv('GOOGLE_SERVICE_ACCOUNT')
db_config = AWSConfig(service_name='dynamodb', endpoint_url=getenv('ENDPOINT_DB'))
bucket_config = AWSConfig(service_name='s3', endpoint_url=getenv('ENDPOINT_S3'))