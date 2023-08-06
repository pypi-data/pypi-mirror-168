from typing import Sequence

import disnake

from causar import Transaction, TransactionTypes
from causar.typings import ui


class MessageSent(Transaction):
    def __init__(
        self,
        content: str | None = None,
        *,
        embed: disnake.Embed | None = None,
        embeds: list[disnake.Embed] = None,
        file: disnake.File | None = None,
        files: list[disnake.File] = None,
        allowed_mentions: disnake.AllowedMentions | None = None,
        view: disnake.ui.View | None = None,
        components: ui.Components[ui.MessageUIComponent] | None = None,
        tts: bool = False,
        ephemeral: bool = False,
        suppress_embeds: bool = False,
        delete_after: float | None = None,
        stickers: Sequence[disnake.GuildSticker | disnake.StickerItem] = None,
        nonce: str | int = None,
        reference: disnake.Message
        | disnake.MessageReference
        | disnake.PartialMessage = None,
        mention_author: bool = None,
    ):
        super().__init__(TransactionTypes.MESSAGE_SENT)
        self.tts: bool = tts
        self.nonce: str | int = nonce
        self.ephemeral: bool = ephemeral
        self.content: str | None = content
        self.file: disnake.File | None = file
        self.embed: disnake.Embed | None = embed
        self.view: disnake.ui.View | None = view
        self.mention_author: bool = mention_author
        self.suppress_embeds: bool = suppress_embeds
        self.delete_after: float | None = delete_after
        self.files: list[disnake.File] = files if files else []
        self.embeds: list[disnake.Embed] = embeds if embeds else []
        self.allowed_mentions: disnake.AllowedMentions | None = allowed_mentions
        self.components: ui.Components[ui.MessageUIComponent] | None = components
        self.stickers: Sequence[disnake.GuildSticker | disnake.StickerItem] = stickers
        self.reference: disnake.Message | disnake.MessageReference | disnake.PartialMessage = (
            reference
        )
