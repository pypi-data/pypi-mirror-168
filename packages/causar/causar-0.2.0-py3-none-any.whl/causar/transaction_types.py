from enum import IntEnum


class TransactionTypes(IntEnum):
    INTERACTION_RESPONSE_SENT = 1
    INTERACTION_FOLLOWUP_SENT = 2
    GET_CHANNEL = 3
    FETCH_CHANNEL = 4
    MESSAGE_SENT = 5
