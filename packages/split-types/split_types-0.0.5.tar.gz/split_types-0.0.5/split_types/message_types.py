from typing import Union

from .transaction import TransactionMessage
from .user import UserMessage


Message = Union[
    TransactionMessage,
    UserMessage,
]
