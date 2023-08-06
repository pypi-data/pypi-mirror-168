from __future__ import annotations

from disnake.ext import commands
from disnake.ext.commands import InvokableSlashCommand, InteractionBot

from causar import Injection, Faker, Cache


class Causar:
    def __init__(self, bot: InteractionBot, *, random_seed: int | None = None):
        self.bot: InteractionBot = bot
        self.faker: Faker = Faker(self, random_seed)
        self.cache: Cache = Cache(self)

    async def run_command(
        self,
        injection: Injection,
    ):
        """Invoke a command and return a list of transactions which occurred."""
        command: InvokableSlashCommand = self.bot.get_slash_command(
            injection.command_name
        )
        try:
            await command.invoke(injection.as_interaction())
        except commands.CommandInvokeError as e:
            raise e

    async def generate_injection(self, command_name: str) -> Injection:
        return Injection(self, command_name=command_name)
