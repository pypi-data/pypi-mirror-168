from typing import Optional

from pydantic import BaseModel

from pydantic_lambda_handler.main import PydanticLambdaHandler


def test_gen_event_model():
    """should work with an empty event"""

    class EventModel(BaseModel):
        path: dict[str, str]
        query: dict[str, str]
        body: Optional[dict[str, str]]

    PydanticLambdaHandler._gen_event_model({}, EventModel)
