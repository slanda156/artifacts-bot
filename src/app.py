from logging import getLogger
from pathlib import Path


logger = getLogger(__name__)


from src.character import Character
from src.server import Server
from src.jobs import CHARACTERJOBMAP


class App:
    def __init__(self) -> None:
        self.logEmpty()
        logger.info("Starting App")
        # Initialize server
        self.url = "https://api.artifactsmmo.com"
        self.tokenPath = Path.cwd() / Path("keys/token.txt")
        with open(self.tokenPath, "r") as f:
            token = f.read().strip()
        self.server = Server(self.url, token)
        # Initialize characters
        self.characterNames: list[str] = []
        for character in self.server.getCharacters():
            self.characterNames.append(character.name)
        self.characters: dict[str, Character] = {}
        for character in self.characterNames:
            job = CHARACTERJOBMAP[character.lower()]
            self.characters[character] = Character(self.server, character, job)


    def run(self) -> None:
        while True:
            for character in self.characters.values():
                character.run()


    def logEmpty(self) -> None:
        with open("logs/log.log", "a") as f:
            f.write("-" * 120 + "\n")
