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


class RequestResponse(BaseModel):
    message: str
    request: TransactionResponse
    

def username_validator(username: str) -> str:
    if not (2 < len(username) < 17):
        raise ValueError(
            "Username length must be less than 17 and more than 2 characters."
        )

    if not username.isascii():
        raise ValueError("Username must containt ASCII characters only.")

    if " " in username:
        raise ValueError("Username must not containt spaces.")

    if not username[0].isalpha():
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
    card_token: str = Field(max_length=1024)


class AccessTokenResponse(BaseModel):
    access_token: str
    exp: datetime


class BaseUser(BaseModel):
    username: str


class UserRequest(BaseUser):
    pass


class UserResponse(BaseUser):
    id: int


class BaseAcquaintance(BaseModel):
    acquaintance_name: str = Field(min_length=1, max_length=200)
    notes_on_acquaintance: str = Field(max_length=4096)


class AcquaintanceRequest(BaseAcquaintance):
    username: str

class AcquaintanceResponse(BaseAcquaintance):
    model_config = ConfigDict(from_attributes=True)

    id: int

