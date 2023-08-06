import disnake


class TextChannelC(disnake.TextChannel):
    """Purely so we can overload read-only methods."""

    def __class__(self):
        return disnake.TextChannel
