import time
from logging import getLogger
from typing import TYPE_CHECKING, Union


logger = getLogger(__name__)


from src.characterClasses import Skills, Stats, Equipment, Task, Inventory
from src.dataclasses import CharInfo, JobInfo, StateInfo

if TYPE_CHECKING:
    from src.server import Server


RESOURCE = [
    {
        "place": "iron_rocks",
        "ore": "iron_ore",
        "ingot": "iron",
    },
    {
        "place": "copper_rocks",
        "ore": "copper_ore",
        "ingot": "copper",
    }
]


class Character:
    def __init__(self, server: "Server", name: str, job: JobInfo) -> None:
        self.server = server
        self.name = name
        self.job = job
        self._state: Union[StateInfo, None] = None
        self.lastState: Union[StateInfo, None] = None
        self.maxLevel = 0
        self.currentResource: dict[str, str] = RESOURCE[1]
        self.lastRun = time.time()
        self.lastRefresh = -1.0
        self.maxTime = 1.0
        self.cooldown = 0.0
        self.level = -1
        self.levelUp = False
        self.xp = -1
        self.maxXp = -1
        self.gold = -1
        self.position: tuple[int, int] = (0, 0)
        self._charInfo: Union[CharInfo, None] = None
        self._skills: Skills = Skills()
        self._stats: Stats = Stats()
        self._equipment: Equipment = Equipment()
        self._task: Task = Task()
        self._inventory: Inventory = Inventory()
        self.server.addChild(self)
        self.refreshCharacter()


    def refreshCharacter(self) -> None:
        timeSineLastRefresh = time.time() - self.lastRefresh
        if timeSineLastRefresh > self.maxTime or self.lastRefresh < 0:
            logger.info(f"Getting character info for {self.name}")
            self.server.refreshCharacters()


    def update(self, charInfo: CharInfo) -> None:
        self._lastCharInfo = self._charInfo
        self._charInfo = charInfo
        # Update character info
        self.position = (charInfo.x, charInfo.y)
        self.level = charInfo.level
        self.xp = charInfo.xp
        self.maxXp = charInfo.max_xp
        self.gold = charInfo.gold
        # Update character dataclasses
        self._skills.update(charInfo, self.maxLevel)
        self._stats.update(charInfo)
        self._equipment.update(charInfo)
        self._task.update(charInfo)
        self._inventory.update(charInfo.inventory, charInfo.inventory_max_items)
        # Check for level up
        if self._lastCharInfo is not None:
            self.levelUp = self._charInfo.level > self._lastCharInfo.level

        self.lastRefresh = time.time()


    @property
    def inventory(self) -> Inventory:
        self.server.refreshCharacters()
        return self._inventory


    @property
    def state(self) -> Union[StateInfo, None]:
        return self._state

    @state.setter
    def state(self, state: Union[StateInfo, None]) -> None:
        self._state = state
        if state is not None:
            logger.info(f"{self.name} new state: \"{state.state}\" at {state.target}")


    def run(self) -> None:
        self.cooldown -= time.time() - self.lastRun
        self.lastRun = time.time()
        if self.cooldown <= 0:
            logger.info(f"Running {self.name}")
            if self.state is not None:
                match self.state.state:
                    case "gathering":
                        if self.checkPosition(self.state.target):
                            self.gather(self.state)
                        else:
                            self.lastState = self.state
                            self.state = StateInfo("moving", self.state.target)

                    case "crafting":
                        if self.checkPosition(self.state.target):
                            self.craft(self.state)
                        else:
                            self.lastState = self.state
                            self.state = StateInfo("moving", self.state.target)

                    case "fighting":
                        if self.checkPosition(self.state.target):
                            self.fight(self.state)
                        else:
                            self.lastState = self.state
                            self.state = StateInfo("moving", self.state.target)

                    case "moving":
                        if not self.checkPosition(self.state.target):
                            self.move(self.state.target)
                        else:
                            self.state = None

                    case _:
                        logger.error(f"Unknown state {self.state.state}")
                        self.state = None
            else: #TODO: Implement deciding new state
                if self.lastState is not None:
                    self.state = self.lastState
                    self.lastState = None
                else: #Temporary
                    target = self.server.getNearest(self.position, "workshop", "mining")
                    if target is not None:
                        self.state = StateInfo("crafting", target, self.currentResource["ingot"], 90)
                if self.state is None:
                    self.cooldown = 5.0
                    logger.error(f"No state found for {self.name}")


    def checkPosition(self, target: tuple[int, int]) -> bool:
        return self.position == target


    def move(self, target: tuple[int, int]) -> None:
        if self.server.move(self.name, target):
            self.state = None


    def gather(self, state: StateInfo) -> None:
        item = self.inventory.get(state.code)
        if item is not None:
            remaining = state.amount - item.quantity
        else:
            remaining = state.amount
        if remaining <= 0:
            self.state = None
        else:
            self.server.gather(self.name)


    def craft(self, state: StateInfo) -> None: #TODO: Temporary implementation, needs to be updated
        item = self.inventory.get(self.currentResource["ore"])
        if item is not None and item.quantity // 8 > 0:
            self.server.craft(self.name, state.code, item.quantity // 8)
        else:
            self.lastState = self.state
            target = self.server.getNearest(self.position, "resource", self.currentResource["place"])
            if item is not None:
                amount = (state.amount - item.quantity) * 8
            else:
                amount = state.amount * 8
            amount = min(amount, self.inventory.freeSlots)
            if target is not None:
                self.state = StateInfo("gathering", target, self.currentResource["ore"], amount)
            else:
                logger.critical("No target found")
                raise Exception("No target found")


    def fight(self, state: StateInfo) -> None:
        pass
