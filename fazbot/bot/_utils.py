from typing import TYPE_CHECKING, Any, Callable, TypeVar
from datetime import datetime
from dateparser import parse

P = TypeVar('P')

if TYPE_CHECKING:
    from nextcord import Guild, Interaction, PartialMessageable, User, Thread
    from nextcord.abc import PrivateChannel, GuildChannel
    from nextcord.ext.commands import Bot, Context


class Utils:

    @staticmethod
    async def parse_big_int(interaction: Interaction[Any], value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into an integer.")

    @staticmethod
    async def parse_date(interaction: Interaction[Any], value: str) -> datetime | None:
        try:
            return parse(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into a date.")

    @staticmethod
    async def must_get_channel(bot: Bot, ctx: Context[Any] | Interaction[Any], channel_id: str) -> GuildChannel | Thread | PrivateChannel | PartialMessageable | None:
        return await Utils.must_getter(bot.get_channel, ctx, channel_id, "channel")

    @staticmethod
    async def must_get_guild(bot: Bot, ctx: Context[Any] | Interaction[Any], guild_id: str) -> Guild | None:
        return await Utils.must_getter(bot.get_guild, ctx, guild_id, "guild")

    @staticmethod
    async def must_get_user(bot: Bot, ctx: Context[Any] | Interaction[Any], user_id: str) -> User | None:
        return await Utils.must_getter(bot.get_user, ctx, user_id, "user")

    @staticmethod
    async def must_getter(getter_func: Callable[[int], P | None], ctx: Context[Any] | Interaction[Any], id_: str, type: str) -> P | None:
        try:
            id__ = int(id_)
        except ValueError:
            await ctx.send(f"Failed parsing {id_} into an integer.")
            return
        if not id__:
            return
        if not (user := getter_func(id__)):
            await ctx.send(f"{type.title()} with ID `{id__}` not found.")
            return
        return user
