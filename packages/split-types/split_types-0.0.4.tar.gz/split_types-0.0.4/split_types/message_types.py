from typing import List, Literal, Tuple, TypedDict, Union


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


class StoreTransactionMessageDataComponent(TypedDict):
    payer_id: str
    payee_id: str
    amount: str


class StoreTransactionMessageData(TypedDict):
    date: str
    description: str
    components: List[StoreTransactionMessageDataComponent]

StoreTransactionMessage = Tuple[Literal['store_transaction'], StoreTransactionMessageData]

class GetTokenMessageData(TypedDict):
    email: str
    password: str

GetTokenMessage = Tuple[Literal['get_token'], GetTokenMessageData]


Message = Union[
    CreateUserMessage,
    StoreUserMessage,
    GetTokenMessage,
]
