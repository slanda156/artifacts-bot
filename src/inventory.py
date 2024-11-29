import time
from logging import getLogger
from typing import TYPE_CHECKING


logger = getLogger(__name__)


if TYPE_CHECKING:
    from src.server import Server


class Inventory:
    def __init__(self, server: "Server", name: str):
        self.server = server
        self.name = name
        self.lastRefresh = -1.0
        self._items: list[dict] = []
        self.maxTime = 1
        self.fill = 0.0
        self.maxSlots = 0
        self.slots = 0
        self.server.addChild(self)


    @property
    def items(self) -> list[dict]:
        timeSinceLast = time.time() - self.lastRefresh
        if timeSinceLast > self.maxTime or self.lastRefresh < 0:
            logger.info(f"Getting inventory for {self.name}")
            self.server.refreshInventorys()
        return self._items
