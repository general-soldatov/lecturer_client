import boto3
import logging
import json
import boto3.session
from progress.bar import IncrementalBar
from os import getenv
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta
from typing import Dict
from app.connect.gsheet import UserSheet
from app.config.configure import AWSSession, AWSConfig, Configure, Session

logger = logging.getLogger(__name__)

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
        self.s3 = self.connect_to_boto(session_aws, configure)
        self.bucket_name = bucket_name
        self.temp_path = 'app/temp'

    @staticmethod
    def connect_to_boto(session_aws: dict, configure: dict):
        try:
            return boto3.session.Session(**session_aws).resource(**configure)
        except Exception as err:
            logger.error(err)

    @staticmethod
    def path_name(path=None, name='name.json'):
        return f'{path}/{name}' if path else name

    def json_upload(self, data: dict, path=None, name='name.json'):
        schedule = json.dumps(data, ensure_ascii=False, indent=4)
        self.s3.Object(self.bucket_name, self.path_name(path, name)).put(Body=schedule)
        logger.info(f'File {name} upload to bucket {self.bucket_name}')

    def json_download(self, path, filename):
        try:
            get_object_response = self.s3.Object(self.bucket_name, self.path_name(path, filename)).get()
            return json.loads(get_object_response['Body'].read())
        except Exception as e:
            logger.error(e)
            return {}



class BucketClient(BucketManage):
    def __init__(self, bucket_name, config, session_aws = None):
        super().__init__(bucket_name, config, session_aws)
        self.td = TodoistAPI(getenv('TODOIST'))

    def schedule(self, path='json', name='schedule.json', todo="to-do.json"):
        """Функция конвертации расписания из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(self.config).schedule()
        self.bar = IncrementalBar("Upload shedule", max = 7, suffix='%(percent)d%%')
        self.json_upload(data, path, name)
        self.bar.next(2)
        self.td_list: dict = self.json_download(path, todo)
        self.bar.next(2)
        self._del_tasks()
        self.bar.finish()
        self.add_todoist(data)
        self.json_upload(self.td_list, path, todo)


    def _del_tasks(self):
        for task in self.td_list['tasks']:
            self.td.delete_task(task)
        self.td_list['tasks'].clear()
        self.bar.next(3)

    def contingent(self, path='json', name='contingent.json'):
        """Функция конвертации контингента из GoogleSheet в json-формат на бакете Yandex Cloud
        """
        data = UserSheet(self.config).contingent(subject_bot=self.bucket_name)
        self.json_upload(data, path, name)

    def add_todoist(self, schedule: Dict[str, Dict[str, Dict[str, str]]]):
        now = datetime.now()
        start = now - timedelta(days=now.weekday())
        print("Upload shedule to")
        for i in range(2):
            day = start + timedelta(days=i * 7)
            delimiter = (day.isocalendar().week + 1) % 2
            info = schedule[str(delimiter)].values()
            bar = IncrementalBar(f"{2 - delimiter} week",
                                 max = len(info), suffix='%(percent)d%%')
            for j, today in enumerate(info):
                day_to = day + timedelta(days=j)
                for key, value in today.items():
                    time = key.replace('.', ':') .split(sep='-')
                    text = f"{value} до {time[1]}"
                    hour, minute = map(int, time[0].split(sep=':'))
                    day_to = day_to.replace(hour=hour, minute=minute)
                    task = self.td.add_task(text,
                                            project_id=self.td_list['projects']['vsau'],
                        due_string='every 2 week',
                        due_datetime=day_to)
                    self.td_list['tasks'].append(task.id)
                bar.next()
            bar.finish()
