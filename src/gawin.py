from logging import getLogger

import httpx


logger = getLogger(__name__)

with open("../keys/token.txt", "r") as f:
    token = f.read().strip()

server = "https://api.artifactsmmo.com"
character = "Gawin"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}


def fight() -> int:
    logger.info("Fighting")
    url = f"{server}/my/{character}/action/fight"
    response = httpx.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error while fighting: {response.status_code}")
        logger.debug(response.json())
        return 5
    data = response.json()["data"]
    return data["cooldown"]["total_seconds"]


def heal() -> tuple[int, int]:
    logger.info("Healing")
    url = f"{server}/my/{character}/action/rest"
    response = httpx.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error while healing: {response.status_code}")
        logger.debug(response.json())
        return 5, 1
    data = response.json()["data"]
    return data["cooldown"]["total_seconds"], data["character"]["max_hp"] - data["character"]["hp"]


def move(pos: tuple[int, int]) -> tuple[int, bool]:
    logger.info(f"Moving to {pos}")
    url = f"{server}/my/{character}/action/move"
    data = {
        # "body": "{\"x\":" + str(pos[0]) + ",\"y\":" + str(pos[1]) + "}"
        "body": {
            "x": pos[0],
            "y": pos[1]
        }
    }
    response = httpx.post(url, headers=headers, data=data)
    if response.status_code != 200:
        logger.error(f"Error while moving: {response.status_code}")
        logger.debug(response.json())
        return 5, False
    data = response.json()["data"]
    arrived = False
    if data["character"]["x"] == pos[0] and data["character"]["y"] == pos[1]:
        arrived = True
    return data["cooldown"]["total_seconds"], arrived


def chopTrees() -> int:
    logger.info("Chopping trees")
    url = f"{server}/my/{character}/action/gathering"
    response = httpx.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error while chopping: {response.status_code}")
        logger.debug(response.json())
        if response.status_code == 499:
            cooldown = float(response.json()["error"]["message"][23:-14])
            return int(cooldown)
        return 5
    data = response.json()["data"]
    return data["cooldown"]["total_seconds"]


def getInventory():
    logger.info("Getting inventory")
    url = f"{server}/my/characters"
    response = httpx.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error while getting inventory: {response.status_code}")
        logger.debug(response.json())
        return []
    characters = response.json()["data"]
    for char in characters:
        if char["name"] == character:
            logger.debug(char["inventory"])
            return char["inventory"]
