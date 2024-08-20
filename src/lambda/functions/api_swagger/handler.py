from aws_lambda_powertools.event_handler.openapi.params import Body
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import Logger

from models import CreateOrderRequest, CreateOrderOutput, InternalServerErrorOutput

logger = Logger()
app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(path="/swagger", title="AWS Lambda Handler Cookbook - Orders Service")


@app.post(
    "/api/orders/",
    summary="Create an order",
    description="Create an order identified by the body payload",
    response_description="The created order",
    responses={
        200: {
            "description": "The created order",
            "content": {"application/json": {"model": CreateOrderOutput}},
        },
        501: {
            "description": "Internal server error",
            "content": {"application/json": {"model": InternalServerErrorOutput}},
        },
    },
    tags=["CRUD"],
)
def handle_create_order(
    create_input: Annotated[CreateOrderRequest, Body(embed=False, media_type="application/json")]
) -> CreateOrderOutput:
    return CreateOrderOutput(name="test", item_count=100, id=1)


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
