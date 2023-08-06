from __future__ import annotations

import datetime
import random
import string
from typing import TYPE_CHECKING, Union, Type, overload

import disnake

from causar import InjectionMetadata, overloads
from causar.typings import overwrites

if TYPE_CHECKING:
    from causar import Causar


# noinspection PyMethodMayBeStatic
class Faker:
    def __init__(self, causar: Causar, seed: int | None):
        self.causar: Causar = causar
        self._seed: int | None = seed

        if self._seed:
            random.seed(self._seed)

    @property
    def bot_state(self):
        return self.causar.bot._connection

    def _generate_b64(self, *, length: int = 214, has_upper=False) -> str:
        # 214 at time of impl
        if not has_upper:
            return "".join(
                random.choices(string.ascii_lowercase + string.digits, k=length)
            )
        else:
            return "".join(
                random.choices(
                    string.ascii_lowercase + string.digits + string.ascii_uppercase,
                    k=length,
                )
            )

    def _deconstruct_snowflake(self, snowflake: int):
        timestamp = (snowflake >> 22) + 1420070400000
        worker = (snowflake & 0x3E0000) >> 17
        process = (snowflake & 0x1F000) >> 12
        increment = snowflake & 0xFFF

        return timestamp, worker, process, increment

    def _generate_snowflake_raw(
        self, timestamp: int, worker: int, process: int, increment: int
    ) -> int:
        """Create a realistic snowflake

        Parameters
        ----------
        timestamp: int
            Milliseconds
        worker: int
            5 bit integer
        process: int
            5 bit integer
        increment: int
            12
        """
        snowflake = (
            ((timestamp - 1420070400000) << 22)
            | (worker << 17)
            | (process << 12)
            | increment
        )
        return snowflake

    def generate_snowflake(self, timestamp: int | None = None) -> str:
        return str(random.randint(100000000000000000, 999999999999999999))

    @overload
    def generate_member(self, default_member=True) -> disnake.Member:
        ...

    @overload
    def generate_member(
        self, guild: disnake.Guild, default_member=True
    ) -> disnake.Member:
        ...

    def generate_member(
        self,
        *,
        default_member: bool = False,
        guild: disnake.Guild | None = None,
    ) -> disnake.Member:
        if guild is None:
            guild = self.generate_guild(guild_id=881118111967883295)

        if default_member:
            return disnake.Member(
                data={
                    "user": {
                        "username": "Skelmis",
                        "public_flags": 256,
                        "id": "271612318947868673",
                        "discriminator": "9135",
                        "avatar_decoration": None,
                        "avatar": self._generate_b64(length=32),
                    },
                    "roles": [],
                    "premium_since": None,
                    "permissions": "4398046511103",
                    "pending": False,
                    "nick": "Ethan",
                    "mute": False,
                    "joined_at": "2020-09-18T23:14:06.680000+00:00",
                    "is_pending": False,
                    "flags": 0,
                    "deaf": False,
                    "communication_disabled_until": None,
                    "avatar": None,
                },
                guild=guild,
                state=self.causar.bot._connection,
            )

    def generate_guild(
        self,
        *,
        guild_id: int | str,
        unavailable: bool = True,
        owner_id: int | None = None,
    ) -> disnake.Guild:
        data = (
            {"unavailable": unavailable, "id": str(guild_id)} if unavailable else {}
        )  # TODO Guilds with intents lol
        guild = disnake.Guild(data=data, state=self.causar.bot._connection)
        if owner_id:
            guild.owner_id = owner_id

        default_role = self.generate_role(is_default_guild_role=True, guild=guild)
        guild._roles[default_role.id] = default_role

        return guild

    def generate_role(
        self, is_default_guild_role: bool = False, guild: disnake.Guild | None = None
    ):
        if is_default_guild_role:
            data = {
                "id": str(guild.id),
                "name": "@everyone",
                "permissions": "968552730176",
                "position": 0,
                "color": 0,
                "hoist": False,
                "managed": False,
                "mentionable": False,
                "icon": None,
                "unicode_emoji": None,
                "flags": 0,
            }
            return disnake.Role(data=data, state=self.bot_state, guild=guild)

    def generate_channel(
        self,
        *,
        channel_id: int | None = None,
        channel_name: str = "Unknown",
        position: int = 1,
        flags: int = 0,
        parent_id: int | None = None,
        last_message_id: int | None = None,
        topic: str | None = None,
        guild_id: int | None = None,
        rate_limit_per_user: int | None = None,
        nsfw: bool = False,
        cls: Union[
            Type[disnake.TextChannel],
            Type[disnake.DMChannel],
            Type[disnake.Thread],
        ] = disnake.TextChannel,
        permission_overwrites: list[overwrites.PermissionsOverwrite] = None,
    ) -> Union[disnake.TextChannel, disnake.DMChannel, disnake.Thread]:
        # Better support for DM types and don't pass guild_id yada yada
        channel_id: str = str(channel_id) if channel_id else self.generate_snowflake()
        last_message_id: str = (
            str(last_message_id) if last_message_id else self.generate_snowflake()
        )
        guild_id: str = str(guild_id) if guild_id else self.generate_snowflake()
        permission_overwrites: list[overwrites.PermissionsOverwrite] = (
            permission_overwrites if permission_overwrites else []
        )
        data = {
            "id": channel_id,
            "last_message_id": last_message_id,
            "type": 0,
            "name": channel_name,
            "position": position,
            "flags": flags,
            "parent_id": parent_id,
            "topic": topic,
            "guild_id": guild_id,
            "permission_overwrites": permission_overwrites,
            "rate_limit_per_user": rate_limit_per_user,
            "nsfw": nsfw,
        }
        if cls == disnake.TextChannel:
            channel = overloads.TextChannelC(
                data=data,
                guild=self.generate_guild(guild_id=guild_id, unavailable=True),
                state=self.causar.bot._connection,
            )

        elif cls == disnake.DMChannel:
            channel = disnake.DMChannel(
                data=data,
                me=self.causar.bot.user,
                state=self.causar.bot._connection,
            )

        elif cls == disnake.Thread:
            channel = disnake.Thread(
                data=data,
                guild=self.generate_guild(guild_id=guild_id, unavailable=True),
                state=self.causar.bot._connection,
            )
        else:
            raise ValueError("Invalid cls provided.")

        return channel

    def generate_interaction(
        self,
        *,
        kwargs: list[dict],
        metadata: InjectionMetadata,
        author_data: dict,
    ) -> disnake.ApplicationCommandInteraction:
        # TODO Replace with custom guilds, channels etc
        data = {
            "version": 1,
            "type": 2,
            "token": self._generate_b64(has_upper=True),
            "member": author_data,
            "locale": "en-US",
            "id": "1016666832901517383",
            "guild_locale": "en-US",
            "guild_id": metadata.guild_id,
            "data": {
                "type": 1,
                "options": kwargs,
                "name": metadata.command_name,
                "id": self.generate_snowflake(),
                "guild_id": metadata.guild_id,
            },
            "channel_id": metadata.channel_id,
            "application_id": "846324706389786676",
            "app_permissions": "4398046511103",
        }
        aci: disnake.ApplicationCommandInteraction = (
            disnake.ApplicationCommandInteraction(
                state=self.causar.bot._connection, data=data
            )
        )
        return aci
