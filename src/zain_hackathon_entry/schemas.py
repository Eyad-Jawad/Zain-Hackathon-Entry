from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserRequest(BaseModel):
    id: int | None
    name: str | None
    card_token: str | None

    @model_validator(mode="after")
    def is_all_none(self) -> Self:
        if not self.id and not self.name and not self.card_token:
            raise ValueError(
                "All values are None. You have to provide at least one value"
            )

        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    card_token: str


class BaseTransaction(BaseModel):
    amount: int
    sender_id: int
    receiver_id: int


class TransactionReqeust(BaseTransaction):
    pass


class TransactionResponse(BaseTransaction):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime


class BaseAuth(BaseModel):
    username: str = Field(min_length=3, max_length=16)
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
