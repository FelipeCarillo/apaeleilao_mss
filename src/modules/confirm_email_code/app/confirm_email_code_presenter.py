import os

from .confirm_email_code_controller import ConfirmEmailCodeController
from .confirm_email_code_usecase import ConfirmEmailCodeUsecase

from src.shared.https_codes.https_code import HttpResponse, HttpRequest
from src.shared.database.database_user_table import UserDynamodb
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock

stage = os.environ.get("STAGE", "test")
if stage == "test":
    usecase = ConfirmEmailCodeUsecase(UserRepositoryMock())
else:
    usecase = ConfirmEmailCodeUsecase(UserDynamodb())
controller = ConfirmEmailCodeController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(auth=event['headers'], body=event['body'])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()
