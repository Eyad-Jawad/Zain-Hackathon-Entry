from datetime import datetime
from typing_extensions import Self
from typing import Annotated

from pydantic import BaseModel, AfterValidator, ConfigDict, model_validator


def luhn_validation(number: int) -> bool:
    num = [int (n) for n in str(number)]

    if not (12 <= len(num) <= 19):
        raise ValueError("Invalid card number, please check again.")

    sum = 0
    for i in range(len(num)):
        offset_from_end = len(num) - i

        if offset_from_end % 2 == 1:
            sum += num[i]
        elif num[i] < 5:
            sum += num[i] * 2
        else:
            sum += num[i] * 2 - 9

    if sum % 10 != 0:
        raise ValueError("Invalid card number, please check again.")

    return number


class UserRequest(BaseModel):
    id: int | None
    name: str | None
    card_number: None | Annotated[int, AfterValidator(luhn_validation)]

    @model_validator(mode="after")
    def is_all_none(self) -> Self:
        if (
            not self.id and
            not self.name and
            not self.card_number
        ):
            raise ValueError(
                "All values are None. You have to provide at least one value"
            )

        return self
    
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    card_number: Annotated[int, AfterValidator(luhn_validation)]


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

