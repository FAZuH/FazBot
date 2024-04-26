# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Generator, Self

from discord.ext.commands import Cog
from discord.ext.commands.hybrid import HybridAppCommand, HybridCommand

if TYPE_CHECKING:
    from discord import Guild
    from fazbot import Core, Bot


class CogBase(Cog):

    def __init__(self, bot: Bot, app: Core, guilds: list[Guild]) -> None:
        self._bot = bot
        self._app = app
        self._guilds = guilds
        self._setup()

    def walk_hybrid_app_commands(self) -> Generator[HybridAppCommand[Self, ..., Any], None, None]:
        for cmd in self.walk_commands():
            if isinstance(cmd, HybridCommand) and cmd.app_command:
                yield cmd.app_command

    async def load_commands(self) -> None:
        """
        Setup method to be called in setup() method on subclasses.
        Adds commands to bot's CommandTree.
        """
        cmds = {*self.walk_hybrid_app_commands(), *self.walk_app_commands()}
        for cmd in cmds:
            self._bot.bot.tree.add_command(cmd, guilds=self._guilds, override=True)
            self._app.logger.console_logger.info(f"Added app command: {cmd.qualified_name}")

        await self._bot.bot.add_cog(self)

    def _setup(self) -> None:
        """
        Method to be run on cog initialization.
        """
        pass
