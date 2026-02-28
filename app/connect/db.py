import boto3
import requests
import json
import logging
from boto3.dynamodb.conditions import Key
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client/.env")

logger = logging.getLogger(__name__)

class UserVar:
    def __init__(self, subject):
        urls = {'termex': 'ENDPOINT_DB', 'phys': 'ENDPOINT'}
        self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=getenv(urls[subject]),
                region_name=getenv('REGION_NAME'),
                aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY')
                )
        self.table = 'User_Var'

    def create_table(self):
        table = self.dynamodb.create_table(
            TableName = self.table,
            KeySchema = [
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Ключ партицирования
                }
            ],
            AttributeDefinitions = [
                {
                "AttributeName": "user_id",
                "AttributeType": "N"
                },
                {
                "AttributeName": "name",
                "AttributeType": "S"
                },
                {
                "AttributeName": "profile",
                "AttributeType": "S"
                },
                {
                "AttributeName": "group",
                "AttributeType": "S"
                },
                {
                "AttributeName": "fine",
                "AttributeType": "N"
                },
                {
                "AttributeName": "prize",
                "AttributeType": "N"
                }

            ]
        )
        return table

    def put_item(self, user_id, name, profile, group, var, var_d1, fine=0, prize=0):
        table = self.dynamodb.Table(self.table)
        all_var = {'var_all': var, 'var_d1': var_d1}
        tasks = {'S0': 0}
        bonus = {
            'static': 0,
            'kinematic': 0,
            'dynamic': 0
        }
        response = table.put_item(
            Item = {
                    'user_id': user_id,
                    'name': name,
                    'profile': profile,
                    'group': group,
                    'var': all_var,
                    'fine': fine,
                    'prize': prize,
                    'tasks': tasks,
                    'bonus': bonus
            }
        )
        return response

    def add_task(self, user_id, task, ball):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set tasks.{task} = :t ",
            ExpressionAttributeValues = {
                ':t': ball
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def set_fine(self, user_id, fine):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set fine = :f ",
            ExpressionAttributeValues = {
                ':f': fine
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def set_prize(self, user_id, prize):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set prize = :p ",
            ExpressionAttributeValues = {
                ':p': prize
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def get_user(self, user_id):
        """Метод запроса информации о пользователе по ключу партицирования
        """
        table = self.dynamodb.Table(self.table)
        response = table.get_item(
            Key = {
                'user_id': user_id
            }
        )
        return response['Item']


    def add_bonus(self, user_id, category, task):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set bonus.{category} = :b ",
            ExpressionAttributeValues = {
                ':b': task
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response


    def all_users(self):
        table = self.dynamodb.Table(self.table)
        return table.scan()['Items']

    def input_users(self):
        table = self.dynamodb.Table(self.table)
        scan_kwargs = {
            'ProjectionExpression': "user_id, name, profile, group"
        }
        response = table.scan(**scan_kwargs)
        return response['Items']


    def for_mailer(self, profile, group):
        """Метод выгрузки ключей таблицы для рассылки
        """
        table = self.dynamodb.Table(self.table)
        scan_kwargs = {
            'ProjectionExpression': "user_id, profile, group"
        }
        response = table.scan(**scan_kwargs)
        try:
            return [int(item['user_id']) for item in response['Items'] if item['profile'] == profile and item['group'] == group]
        except Exception as e:
            logger.error(f'{e}')

    def delete_note(self, user_id: int):
        table = self.dynamodb.Table(self.table)
        try:
            response = table.delete_item(
                Key = {'user_id': user_id},
                )
            return response

        except Exception as e:
            print('Error', e)


    def delete_table(self):
        table = self.dynamodb.Table(self.table)
        table.delete()

def load_contingent(subject, year):
    uv = UserVar(subject)
    data = uv.all_users()
    path = f'{subject}_{year}.json'
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str)
        print('Document', path, 'is complite!')

def order(subject, path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    response = requests.get(f'https://storage.yandexcloud.net/{subject}-bot/json/contingent.json')
    contingent = response.json()
    order_data = []
    contingent_list = [elem for elem in contingent]

    for item in data:
        if item['name'] not in contingent_list:
            order_data.append({'user_id': item['user_id'], 'name': item['name']})
    return order_data