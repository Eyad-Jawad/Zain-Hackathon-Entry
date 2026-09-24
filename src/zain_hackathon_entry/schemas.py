from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


class BaseTransaction(BaseModel):
    amount: int
    receiver_id: int


class TransactionReqeust(BaseTransaction):
    pass


class TransactionResponse(BaseTransaction):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int
    date: datetime


def username_validator(username: str) -> str:
    if not (2 < len(username) < 17):
        raise ValueError(
            "Username length must be less than 17 and more than 2 characters."
        )

    if not username.isascii():
        raise ValueError("Username must containt ASCII characters only.")

    if " " in username:
        raise ValueError("Username must not containt spaces.")

    if username[0].isalpha():
        raise ValueError("Username must start with a character.")

    return username


class BaseAuth(BaseModel):
    username: Annotated[str, AfterValidator(username_validator)]
    password: str = Field(min_length=8, max_length=128)


class LogInRequest(BaseAuth):
    pass


class DeleteAccountRequest(BaseAuth):
    pass


class SignUpRequest(BaseAuth):
    card_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    exp: datetime
