from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from causar import TransactionTypes


class Transaction:
    """A list of transactions is used to represent how something processed."""

    def __init__(self, transaction_type: TransactionTypes):
        self.type: TransactionTypes = transaction_type

    @classmethod
    async def construct(cls, *args, transactions: list, **kwargs):
        instance = cls(*args, **kwargs)
        transactions.append(instance)
        return instance
