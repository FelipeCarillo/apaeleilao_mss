import os
from typing import Any, Dict

from .database import Database

from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface


class UserDynamodb(UserInterface):

    def __init__(self):
        self.__dynamodb = Database().get_table_user()

    def create_user(self, user: User) -> Dict or None:
        try:
            user = user.to_dict()
            user['status_account'] = user['status_account'].value
            self.__dynamodb.put_item(Item=user)
            return {
                'body': user
            }
        except Exception as e:
            raise e

    def authenticate(self, email: str, password: str, user_id: str = None) -> Dict or None:
        try:
            key = {"email": {'S': email}}
            if user_id:
                key.update({"user_id": {'S': user_id}})

            response = self.__dynamodb.get_item(Key=key)
            item = response.get('Item', None)
            if item.get('password', {}).get('S', None) == password:
                return item
            else:
                return None
        except Exception as e:
            raise e

    def get_all_users(self, exclusive_start_key: str = None, limit: int = None) -> Dict or None:
        try:
            response = self.__dynamodb.scan(
                ExclusiveStartKey=exclusive_start_key,
                Limit=limit
            )
            return response.get('Items', None)
        except Exception as e:
            raise e

    def get_user_by_email(self, email) -> Dict or None:
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'email': {
                        'S': email
                    }
                }
            )
            return response.get('Item', None)
        except Exception as e:
            raise e

    def get_user_by_cpf(self, cpf) -> Dict or None:
        try:
            response = self.__dynamodb.scan(
                FilterExpression='cpf = :cpf',
                ExpressionAttributeValues={
                    ':cpf': {
                        'S': cpf
                    }
                }
            )
            return response.get('Items', None)[0]
        except Exception as e:
            raise e

    def update_user(self, user: User):
        pass
