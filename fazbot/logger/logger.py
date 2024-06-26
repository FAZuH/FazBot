from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from . import ConsoleLogger, DiscordLogger, PerformanceLogger


class Logger(Protocol):
    @property
    def console(cls) -> ConsoleLogger: ...
    @property
    def discord(cls) -> DiscordLogger: ...
    @property
    def performance(cls) -> PerformanceLogger: ...
