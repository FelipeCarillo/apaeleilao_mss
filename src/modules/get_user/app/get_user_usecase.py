
from typing import Dict

from src.shared.structure.entities.user import User
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__user_interface = user_interface
        self.__token = TokenAuthy()

    def __call__(self, body: Dict) -> Dict:
        if body.get('Authorization') is None:
            raise UserNotAuthenticated('Token de acesso não encontrado.')

        decoded_token = self.__token.decode_token(body["Authorization"])
        if not decoded_token:
            raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
        user_id = decoded_token.get('user_id')
        user = self.__user_interface.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotAuthenticated()

        status_account_permitted = [STATUS_USER_ACCOUNT_ENUM.ACTIVE, STATUS_USER_ACCOUNT_ENUM.PENDING,
                                    STATUS_USER_ACCOUNT_ENUM.SUSPENDED, STATUS_USER_ACCOUNT_ENUM.BANED]

        if STATUS_USER_ACCOUNT_ENUM(user.get('status_account')) not in status_account_permitted:
            raise UserNotAuthenticated(message='Conta de usuário deletada.')

        user = User(
            user_id=user['user_id'],
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            cpf=user.get('cpf'),
            email=user.get('email'),
            phone=user.get('phone'),
            password=user.get('password'),
            accepted_terms=user.get('accepted_terms'),
            status_account=user.get('status_account'),
            type_account=user.get('type_account'),
            created_at=int(user.get('created_at')) if user.get('created_at') else None,
            verification_email_code=str(user.get('verification_email_code')) if user.get(
                'verification_email_code') else None,
            verification_email_code_expires_at=int(user.get('verification_email_code_expires_at')) if user.get(
                'verification_email_code_expires_at') else None,
        )

        user_dict = user.to_dict()

        if user.status_account == STATUS_USER_ACCOUNT_ENUM.BANED or user.status_account == STATUS_USER_ACCOUNT_ENUM.SUSPENDED:
            user_dict['suspensions'] = self.__user_interface.get_all_suspensions_by_user_id(user_id=user_id)

        user_dict.pop('password')
        return user_dict
