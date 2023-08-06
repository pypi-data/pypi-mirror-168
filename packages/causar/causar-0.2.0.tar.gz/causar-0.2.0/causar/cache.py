from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Union

import disnake

from causar import CacheLookupFailed, Injection, transactions

if TYPE_CHECKING:
    from causar import Causar


class Cache:
    """An abstraction on mocking disnakes internal caches."""

    def __init__(self, causar: Causar):
        self.causar: Causar = causar

        self._users: dict[int, disnake.User] = {}
        self._members: dict[int, disnake.Member] = {}
        self._guilds: dict[int, disnake.Guild] = {}
        self._channels: dict[
            int,
            Union[
                disnake.abc.GuildChannel,
                disnake.abc.PrivateChannel,
                disnake.abc.Thread,
            ],
        ] = {}

    def get_user(self, user_id: int) -> disnake.User:
        try:
            return self._users[user_id]
        except KeyError:
            raise CacheLookupFailed

    def get_member(self, member_id: int) -> disnake.Member:
        try:
            return self._members[member_id]
        except KeyError:
            raise CacheLookupFailed

    def get_guild(self, guild_id: int) -> disnake.Guild:
        try:
            return self._guilds[guild_id]
        except KeyError:
            raise CacheLookupFailed

    def get_channel(
        self, channel_id: int
    ) -> Union[
        disnake.abc.GuildChannel,
        disnake.abc.PrivateChannel,
        disnake.abc.Thread,
    ]:
        try:
            return self._channels[channel_id]
        except KeyError:
            raise CacheLookupFailed

    def remove_user(self, user_id: int) -> Cache:
        self._users.pop(user_id, None)
        return self

    def remove_member(self, member_id: int) -> Cache:
        self._members.pop(member_id, None)
        return self

    def remove_guild(self, guild_id: int) -> Cache:
        self._guilds.pop(guild_id, None)
        return self

    def remove_channel(self, channel_id: int) -> Cache:
        self._channels.pop(channel_id, None)
        return self

    def reset_cache(self) -> Cache:
        self._users = {}
        self._guilds = {}
        self._members = {}
        self._channels = {}
        return self

    def add_user(self, user: disnake.User, injection: Injection) -> Cache:
        self._users[user.id] = user
        return self

    def add_member(self, member: disnake.Member, injection: Injection) -> Cache:
        self._members[member.id] = member
        return self

    def add_guild(self, guild: disnake.Guild, injection: Injection) -> Cache:
        self._guilds[guild.id] = guild
        return self

    def add_channel(
        self,
        channel: Union[
            disnake.abc.GuildChannel,
            disnake.abc.PrivateChannel,
            disnake.abc.Thread,
        ],
        injection: Injection,
    ) -> Cache:
        self._channels[channel.id] = channel
        channel.send = partial(
            transactions.MessageSent.construct, transactions=injection.transactions
        )
        return self

    def bulk_add(
        self,
        *args: list[
            Union[
                disnake.abc.GuildChannel,
                disnake.abc.PrivateChannel,
                disnake.abc.Thread,
                disnake.User,
                disnake.Member,
                disnake.Guild,
            ]
        ],
        injection: Injection,
    ) -> Cache:
        for item in args:
            if isinstance(item, disnake.User):
                self.add_user(item, injection)

            elif isinstance(item, disnake.Member):
                self.add_member(item, injection)

            elif isinstance(item, disnake.Guild):
                self.add_guild(item, injection)

            elif isinstance(
                item,
                (
                    disnake.abc.GuildChannel,
                    disnake.abc.PrivateChannel,
                    disnake.abc.Thread,
                ),
            ):
                self.add_channel(item, injection)

            else:
                raise ValueError(
                    f"{item.__class__.__name__!r} is not a valid item type."
                )

        return self
