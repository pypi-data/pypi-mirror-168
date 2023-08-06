import disnake

from causar import Transaction, TransactionTypes
from causar.typings import ui


class InteractionFollowUpSent(Transaction):
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
        delete_after: float | None = None
    ):
        super().__init__(TransactionTypes.INTERACTION_FOLLOWUP_SENT)
        self.tts: bool = tts
        self.ephemeral: bool = ephemeral
        self.content: str | None = content
        self.file: disnake.File | None = file
        self.embed: disnake.Embed | None = embed
        self.view: disnake.ui.View | None = view
        self.suppress_embeds: bool = suppress_embeds
        self.delete_after: float | None = delete_after
        self.files: list[disnake.File] = files if files else []
        self.embeds: list[disnake.Embed] = embeds if embeds else []
        self.components: ui.Components[ui.MessageUIComponent] | None = components
        self.allowed_mentions: disnake.AllowedMentions | None = allowed_mentions
