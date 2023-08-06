from causar import Transaction, TransactionTypes


class FetchChannel(Transaction):
    def __init__(self, channel_id: int):
        super().__init__(transaction_type=TransactionTypes.FETCH_CHANNEL)
        self.channel_id: int = channel_id
