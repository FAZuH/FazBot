from __future__ import annotations
from contextlib import contextmanager
from threading import Lock
from typing import Generator, TYPE_CHECKING

from fazbot import Asset, Config
from fazbot.bot import DiscordBot
from fazbot.constants import Constants
from fazbot.db.fazbot import FazBotDatabase
from fazbot.logger import FazBotLogger

from .core import Core

if TYPE_CHECKING:
    from fazbot import Bot, Logger, IFazBotDatabase


class FazBot(Core):

    def __init__(self) -> None:
        self._locks: dict[str, Lock] = {}
        self._asset = Asset(Constants.ASSET_DIR)
        self._config = Config()

        self._asset.read_all()
        self._config.read()

        conf = self.config
        self._fazbotdb = FazBotDatabase(
            "mysql+aiomysql",
            conf.mysql_username,
            conf.mysql_password,
            conf.mysql_host,
            conf.mysql_port,
            conf.fazbot_db_name
        )
        self._logger = FazBotLogger(conf.discord_log_webhook, conf.admin_discord_id)
        self._bot = DiscordBot(self)

    def start(self) -> None:
        self._bot.start()

    def stop(self) -> None:
        self._bot.stop()

    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def config(self) -> Config:
        return self._config

    @property
    def logger(self) -> Logger:
        return self._logger

    @contextmanager
    def enter_bot(self) -> Generator[Bot]:
        with self._get_lock("bot"):
            yield self._bot

    @contextmanager
    def enter_fazbotdb(self) -> Generator[IFazBotDatabase]:
        with self._get_lock("fazbotdb"):
            yield self._fazbotdb

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
