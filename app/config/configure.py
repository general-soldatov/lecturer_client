from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

load_dotenv()

@dataclass
class DBConfig:
    endpoint: str
    region_name: str
    key_id: str
    access_key: str
    google_api: str = getenv('GOOGLE_SERVICE_ACCOUNT')