from logging import getLogger
from typing import TYPE_CHECKING
import time

import httpx


logger = getLogger(__name__)


if TYPE_CHECKING:
    from src.inventory import Inventory


class Server:
    def __init__(self, address: str, token: str) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        self.address = address
        self.childs: dict[str, "Inventory"] = {}


    def addChild(self, child: "Inventory") -> None:
        self.childs[child.name] = child


    def refreshInventorys(self) -> None:
        url = f"{self.address}/my/characters"
        response = httpx.get(url, headers=self.headers)
        stat, data = self.checkResponse(response)
        if stat:
            for char in data["data"]:
                self.childs[char["name"]]._items = char["inventory"]
                self.childs[char["name"]].lastRefresh = time.time()
                self.childs[char["name"]].maxSlots = char["inventory_max_items"]
                self.childs[char["name"]].slots = 0
                for item in self.childs[char["name"]]._items:
                    self.childs[char["name"]].slots += item["quantity"]
                self.childs[char["name"]].fill = self.childs[char["name"]].slots / self.childs[char["name"]].maxSlots

        else:
            logger.error("Error while refreshing inventorys")
            logger.debug(data)


    def checkResponse(self, response: httpx.Response) -> tuple[bool, dict]:
        if response.status_code == 200:
            return True, response.json()
        else:
            logger.error(f"Unkown error: {response.status_code}")
            logger.debug(response.json())
            return False, response.json()


    def getServerStatus(self,) -> bool:
        logger.info("Getting server status")
        url = f"{self.address}"
        response = httpx.get(url, headers=self.headers)
        stat, data = self.checkResponse(response)
        if stat:
            return data["data"]["status"]
        return False


    def getCharaters(self,) -> list[str]:
        logger.info("Getting characters")
        url = f"{self.address}/my/characters"
        response = httpx.get(url, headers=self.headers)
        stat, data = self.checkResponse(response)
        if stat:
            return [char["name"] for char in data["data"]]
        return []
