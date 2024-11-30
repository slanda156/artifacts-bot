from logging import getLogger

from pathlib import Path


logger = getLogger(__name__)


from src.character import Character
from src.server import Server


class App:
    def __init__(self) -> None:
        self.url = "https://api.artifactsmmo.com"
        self.tokenPath = Path.cwd() / Path("keys/token.txt")
        with open(self.tokenPath, "r") as f:
            token = f.read().strip()
        self.server = Server(self.url, token)
        self.characterNames = self.server.getCharaters()
        self.characters: dict[str, Character] = {}
        for character in self.characterNames:
            self.characters[character] = Character(self.server, character)


    def run(self) -> None:
        i = 20
        while True:
            for character in self.characters.values():
                character.run()
            i -= 1
            if i < 0:
                break
