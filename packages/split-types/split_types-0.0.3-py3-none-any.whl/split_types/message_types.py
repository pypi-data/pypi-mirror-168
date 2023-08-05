from typing import Literal, Tuple, TypedDict, Union


class CreateUserMessageData(TypedDict):
    email: str
    password: str

CreateUserMessage = Tuple[Literal['create_user'], CreateUserMessageData]


class StoreUserMessageData(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str

StoreUserMessage = Tuple[Literal['store_user'], StoreUserMessageData]

class GetTokenMessageData(TypedDict):
    email: str
    password: str

GetTokenMessage = Tuple[Literal['get_token'], GetTokenMessageData]


Message = Union[
    CreateUserMessage,
    StoreUserMessage,
    GetTokenMessage,
]
