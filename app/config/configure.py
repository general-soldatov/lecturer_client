from dataclasses import dataclass
from os import getenv
from pydantic import BaseModel, Field
import yaml
from typing import List, Dict

class YamlProject(BaseModel):
    @classmethod
    def model_validate_yaml(cls, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as file:
            data = yaml.safe_load(file.read())
            return cls.model_validate(data)

class Endpoints(BaseModel):
    db: str
    s3: str

class AWS(BaseModel):
    endpoints: Endpoints
    default_region: str
    key_id: str
    access_key: str

class TGBot(BaseModel):
    address: str
    token: str

class Discipline(BaseModel):
    bucket_name: str
    tg: TGBot

class GoogleSheet(BaseModel):
    data_path: str

class Configure(YamlProject):
    app: str
    aws: AWS
    discipline: Dict[str, Discipline]
    google: GoogleSheet
    telegram_admin: int

class Session(BaseModel):
    region_name: str = Field(alias="default_region")
    aws_access_key_id: str = Field(alias="key_id")
    aws_secret_access_key: str = Field(alias="access_key")

    @classmethod
    def model_construct(cls, aws: AWS, _fields_set = None, **values):
        return cls(**aws.model_dump())

class AWSConfig(BaseModel):
    service_name: str
    endpoint_url: str

    @classmethod
    def model_construct_s3(cls, config: Configure):
        return cls(service_name='s3', endpoint_url=config.aws.endpoints.s3)

    @classmethod
    def model_construct_db(cls, config: Configure):
        return cls(service_name='dynamodb', endpoint_url=config.aws.endpoints.db)



# load_dotenv()


@dataclass
class AWSSession:
    region_name: str = getenv('AWS_DEFAULT_REGION')
    aws_access_key_id: str = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = getenv('AWS_SECRET_ACCESS_KEY')




# google_api: str = getenv('GOOGLE_SERVICE_ACCOUNT')
# db_config = AWSConfig(service_name='dynamodb', endpoint_url=getenv('ENDPOINT_DB'))
# bucket_config = AWSConfig(service_name='s3', endpoint_url=getenv('ENDPOINT_S3'))
