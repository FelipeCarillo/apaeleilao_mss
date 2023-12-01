from .end_suspension_usecase import EndSuspensionUseCase
from .end_suspension_controller import EndSuspensionController

from src.shared.database.database_user import UserDynamodb
from src.shared.https_codes.https_code import HttpRequest, HttpResponse

usecase = EndSuspensionUseCase(UserDynamodb())
controller = EndSuspensionController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    response = controller(request=request())
    response = HttpResponse(status_code=response.status_code, body=response.body)

    return response.to_dict()