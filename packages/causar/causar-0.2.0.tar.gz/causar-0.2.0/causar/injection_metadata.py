class InjectionMetadata:
    def __init__(
        self,
        *,
        channel_id: int | str,
        guild_id: int | str,
        command_name: str | None = None
    ):
        self.guild_id: str = str(guild_id)
        self.channel_id: str = str(channel_id)

        # Will always be set by the time it's used
        self.command_name: str | None = command_name
