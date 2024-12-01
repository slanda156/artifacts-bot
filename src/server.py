import json
import math
import time
from logging import getLogger
from typing import TYPE_CHECKING, Union
from dataclasses import asdict

import httpx


logger = getLogger(__name__)


from src.dataclasses import CharInfo, InvInfo

if TYPE_CHECKING:
    from src.character import Character


class Server:
    def __init__(self, address: str, token: str) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        self.maxLevel = 0
        self.lastMapRefresh = -1.0
        self.maxMapRefreshTime = 60.0
        self.map: dict[str, dict[tuple[int, int], str]] = {}
        self.address = address
        self.childs: dict[str, "Character"] = {}
        if not self.getServerStatus():
            logger.error("Server is not up")
            raise Exception("Server is not up")
        logger.info("Server is up")
        self.getMap()


    def addChild(self, child: "Character") -> None:
        self.childs[child.name] = child


    def refreshCharacters(self) -> bool:
        charaters = self.getCharacters()
        if not charaters:
            logger.error("No characters found")
            return False
        for char in charaters:
            try:
                self.childs[char.name].maxLevel = self.maxLevel
                self.childs[char.name].update(char)
            except KeyError:
                logger.error(f"Character {char.name} not found")
                logger.debug(f"Character: \n{json.dumps(asdict(char), indent=4)}")
        return True


    def checkResponse(self, response: httpx.Response) -> tuple[bool, dict]:
        if response.status_code == 200:
            return True, response.json()
        #TODO: Add more error handling
        else:
            logger.error(f"Unkown error: {response.status_code}")
            logger.debug(f"Response: \n{json.dumps(response.json(), indent=4)}")
            return False, response.json()


    def getServerStatus(self,) -> bool:
        logger.info("Getting server status")
        url = f"{self.address}"
        response = httpx.get(url, headers=self.headers)
        stat, responseData = self.checkResponse(response)
        if stat:
            self.maxLevel = int(responseData["data"]["max_level"])
            return responseData["data"]["status"]
        return False


    def getCharacters(self,) -> list[CharInfo]:
        logger.info("Getting characters")
        url = f"{self.address}/my/characters"
        response = httpx.get(url, headers=self.headers)
        stat, responseData = self.checkResponse(response)
        if stat:
            chars = []
            for char in responseData["data"]:
                chars.append(self.createCharInfo(char))
            return chars
        return []


    def createCharInfo(self, char: dict) -> CharInfo:
        items = []
        _items = char.pop("inventory")
        for item in _items:
            items.append(InvInfo(**item))
        return CharInfo(inventory=items, **char)


    def getMap(self,) -> None:
        url = f"{self.address}/maps"
        response = httpx.get(url, headers=self.headers)
        stat, responseData = self.checkResponse(response)
        if not stat:
            logger.error("Failed to get map")
            return
        logger.info("Getting map")
        self.map = {}
        self.lastMapRefresh = time.time()
        pages = responseData["pages"]
        for page in range(2, pages + 1):
            response = httpx.get(url + f"?page={page}", headers=self.headers)
            stat, responseData = self.checkResponse(response)
            if not stat:
                logger.error(f"Failed to get map page {page} of {pages}")
                continue
            logger.debug(f"Page {page} of {pages}")
            for tile in responseData["data"]:
                if tile["content"] is None:
                    continue
                tileType = tile["content"]["type"]
                if self.map.get(tileType) is None:
                    self.map[tileType] = {}
                self.map[tileType][(int(tile["x"]), int(tile["y"]))] = str(tile["content"]["code"])


    def getNearest(self, pos: tuple[int, int], type: str, code: str) -> Union[tuple[int, int] , None]:
        timeSineLastRefresh = time.time() - self.lastMapRefresh
        if timeSineLastRefresh > self.maxMapRefreshTime or self.lastMapRefresh < 0:
            self.getMap()
        if type not in self.map.keys():
            logger.warning(f"Type {type} not found in map")
            return None
        logger.info(f"Getting nearest {type}:{code}")
        nearest = None
        minDist = 999999999
        for tile in self.map[type].keys():
            if self.map[type][tile] == code:
                dist = math.sqrt((pos[0] - tile[0]) ** 2 + (pos[1] - tile[1]) ** 2)
                if dist < minDist:
                    minDist = dist
                    nearest = tile
        if nearest:
            return nearest
        return None


    def move(self, character: str, pos: tuple[int, int]) -> bool:
        logger.info(f"Moving {character} to {pos}")
        url = f"{self.address}/my/{character}/action/move"
        data = {"x": pos[0], "y": pos[1]}
        response = httpx.post(url, headers=self.headers, json=data)
        stat, responseData = self.checkResponse(response)
        if not stat:
            logger.error(f"Failed to move {character} to {pos}")
            return False
        self.childs[character].cooldown = responseData["data"]["cooldown"]["remaining_seconds"]
        self.childs[character].update(self.createCharInfo(responseData["data"]["character"]))
        return True


    def gather(self, character: str) -> bool:
        logger.info(f"{character} gathering at {self.childs[character].position}")
        url = f"{self.address}/my/{character}/action/gathering"
        response = httpx.post(url, headers=self.headers)
        stat, responseData = self.checkResponse(response)
        if not stat:
            logger.error(f"Failed to gather {character}")
            return False
        self.childs[character].cooldown = responseData["data"]["cooldown"]["remaining_seconds"]
        self.childs[character].update(self.createCharInfo(responseData["data"]["character"]))
        return True


    def craft(self, character: str, code: str, amount: int) -> bool:
        logger.info(f"{character} crafting {amount}x\"{code}\" at {self.childs[character].position}")
        url = f"{self.address}/my/{character}/action/crafting"
        data = {"code": code, "quantity": amount}
        response = httpx.post(url, headers=self.headers, json=data)
        stat, responseData = self.checkResponse(response)
        if not stat:
            logger.error(f"Failed to craft {character}")
            return False
        self.childs[character].cooldown = responseData["data"]["cooldown"]["remaining_seconds"]
        self.childs[character].update(self.createCharInfo(responseData["data"]["character"]))
        return True
