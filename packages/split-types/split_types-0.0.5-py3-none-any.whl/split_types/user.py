from typing import Literal, Tuple, TypedDict, Union


class User(TypedDict):
    user_id: str
    email: str
    hashed_password: str
    name: str
    creation_time: str
    is_active: bool


class UserToken(TypedDict):
    user_id: str
    email: str
    creation_time: str
    expiry_time: str


StoreUserMessage = Tuple[Literal['store_user'], User]


class CreateUserAndGetTokenMessageData(TypedDict):
    email: str
    password: str
    name: str


CreateUserAndGetTokenMessage = Tuple[Literal['create_user_and_get_token'], CreateUserAndGetTokenMessageData]


class GetTokenMessageData(TypedDict):
    email: str
    password: str


GetTokenMessage = Tuple[Literal['get_token'], GetTokenMessageData]


UserMessage = Union[
    CreateUserAndGetTokenMessage,
    StoreUserMessage,
    GetTokenMessage,
]