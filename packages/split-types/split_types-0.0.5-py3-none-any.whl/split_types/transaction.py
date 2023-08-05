from typing import List, Literal, Tuple, TypedDict, Union


class StoreTransactionMessageDataComponent(TypedDict):
    payer_id: str
    payee_id: str
    amount: str


class StoreTransactionMessageData(TypedDict):
    date: str
    description: str
    components: List[StoreTransactionMessageDataComponent]


StoreTransactionMessage = Tuple[Literal['store_transaction'], StoreTransactionMessageData]


TransactionMessage = StoreTransactionMessage
# TransactionMessage = Union[
#     StoreTransactionMessage,
# ]