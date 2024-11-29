from logging import getLogger
from typing import TYPE_CHECKING


logger = getLogger(__name__)


from src.inventory import Inventory

if TYPE_CHECKING:
    from src.server import Server


class Character:
    def __init__(self, server: "Server", name: str) -> None:
        self.server = server
        self.name = name
        self.inventory = Inventory(self.server, self.name)


    def run(self) -> None:
        logger.info(f"Running {self.name}")
