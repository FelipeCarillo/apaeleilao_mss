from .update_payment_usecase import UpdatePaymentUseCase
from .update_payment_controller import UpdatePaymentController

from src.shared.database.database_auction import AuctionDynamodb
from src.shared.https_codes.https_code import HttpResponse, HttpRequest

usecase = UpdatePaymentUseCase(AuctionDynamodb())
controller = UpdatePaymentController(usecase)


def lambda_handler(event, context):
    request = HttpRequest(body=event["body"])
    response = controller(request=request())
    http_response = HttpResponse(status_code=response.status_code, body=response.body)

    return http_response.to_dict()