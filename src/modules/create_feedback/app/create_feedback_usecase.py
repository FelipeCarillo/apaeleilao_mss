from typing import Dict

from src.shared.structure.entities.feedback import Feedback
from src.shared.helper_functions.token_authy import TokenAuthy
from src.shared.helper_functions.events_trigger import EventsTrigger
from src.shared.structure.interface.user_interface import UserInterface
from src.shared.helper_functions.time_manipulation import TimeManipulation
from src.shared.helper_functions.image_manipulation import ImageManipulation
from src.shared.structure.interface.auction_interface import AuctionInterface
from src.shared.structure.enums.user_enum import STATUS_USER_ACCOUNT_ENUM, TYPE_ACCOUNT_USER_ENUM
from src.shared.errors.modules_errors import DataAlreadyUsed, MissingParameter, UserNotAuthenticated, InvalidParameter


class CreateFeedbackUseCase:
    def __init__(self, user_interface: UserInterface):
        self.__token = TokenAuthy()
        self.__trigger = EventsTrigger()
        self.__user_interface = user_interface

    def __call__(self, auth: Dict, body: Dict) -> None:

        if auth.get("Authorization"):
            decoded_token = self.__token.decode_token(body["Authorization"])
            if not decoded_token:
                raise UserNotAuthenticated("Token de acesso inválido ou expirado.")
            user_id = decoded_token.get('user_id')
            user = self.__user_interface.get_user_by_id(user_id=user_id)
            if not user:
                raise UserNotAuthenticated()
            
        if not body.get("email") and not auth.get("Authorization"):
            raise MissingParameter("Email")
        
        if not body.get('content'):
            raise MissingParameter("Texto")
        
        feedback_id = self.__user_interface.get_last_feedback_id()+1
        email = body.get('email', user.get('email'))
        created_at = TimeManipulation.get_current_time()

        feedback = Feedback(
            feedback_id = feedback_id,
            email = email,
            created_at= created_at,
            content = body.get('content')
        )

        self.__user_interface.create_feedback(feedback)

        return None
