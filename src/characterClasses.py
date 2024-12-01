from logging import getLogger
from typing import Union


logger = getLogger(__name__)


from src.dataclasses import CharInfo, InvInfo, SkillInfo


class Skills:
    def __init__(self) -> None:
        self.mining = SkillInfo("Mining", 0, 0, 0, 0, 0, 0)


    def update(self, char: CharInfo, maxLevel: int) -> None:
        # Mining
        xpToLevel = char.mining_max_xp - char.mining_xp
        try:
            progress = char.mining_xp / char.mining_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.mining = SkillInfo(
            "Mining",
            char.mining_level,
            maxLevel,
            char.mining_xp,
            char.mining_max_xp,
            xpToLevel,
            progress
        )
        # Woodcutting
        xpToLevel = char.woodcutting_max_xp - char.woodcutting_xp
        try:
            progress = char.woodcutting_xp / char.woodcutting_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.woodcutting = SkillInfo(
            "Woodcutting",
            char.woodcutting_level,
            maxLevel,
            char.woodcutting_xp,
            char.woodcutting_max_xp,
            xpToLevel,
            progress
        )
        # Fishing
        xpToLevel = char.fishing_max_xp - char.fishing_xp
        try:
            progress = char.fishing_xp / char.fishing_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.fishing = SkillInfo(
            "Fishing",
            char.fishing_level,
            maxLevel,
            char.fishing_xp,
            char.fishing_max_xp,
            xpToLevel,
            progress
        )
        # Weaponcrafting
        xpToLevel = char.weaponcrafting_max_xp - char.weaponcrafting_xp
        try:
            progress = char.weaponcrafting_xp / char.weaponcrafting_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.weaponcrafting = SkillInfo(
            "Weaponcrafting",
            char.weaponcrafting_level,
            maxLevel,
            char.weaponcrafting_xp,
            char.weaponcrafting_max_xp,
            xpToLevel,
            progress
        )
        # Gearcrafting
        xpToLevel = char.gearcrafting_max_xp - char.gearcrafting_xp
        try:
            progress = char.gearcrafting_xp / char.gearcrafting_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.gearcrafting = SkillInfo(
            "Gearcrafting",
            char.gearcrafting_level,
            maxLevel,
            char.gearcrafting_xp,
            char.gearcrafting_max_xp,
            xpToLevel,
            progress
        )
        # Jewelrycrafting
        xpToLevel = char.jewelrycrafting_max_xp - char.jewelrycrafting_xp
        try:
            progress = char.jewelrycrafting_xp / char.jewelrycrafting_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.jewelrycrafting = SkillInfo(
            "Jewelrycrafting",
            char.jewelrycrafting_level,
            maxLevel,
            char.jewelrycrafting_xp,
            char.jewelrycrafting_max_xp,
            xpToLevel,
            progress
        )
        # Cooking
        xpToLevel = char.cooking_max_xp - char.cooking_xp
        try:
            progress = char.cooking_xp / char.cooking_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.cooking = SkillInfo(
            "Cooking",
            char.cooking_level,
            maxLevel,
            char.cooking_xp,
            char.cooking_max_xp,
            xpToLevel,
            progress
        )
        # Alchemy
        xpToLevel = char.alchemy_max_xp - char.alchemy_xp
        try:
            progress = char.alchemy_xp / char.alchemy_max_xp
        except ZeroDivisionError:
            progress = 1.0
        self.alchemy = SkillInfo(
            "Alchemy",
            char.alchemy_level,
            maxLevel,
            char.alchemy_xp,
            char.alchemy_max_xp,
            xpToLevel,
            progress
        )


class Stats: #TODO Implement stats
    def __init__(self) -> None:
        pass


    def update(self, char: CharInfo) -> None:
        pass


class Equipment: #TODO Implement equipment
    def __init__(self) -> None:
        pass


    def update(self, char: CharInfo) -> None:
        pass


class Task:
    def __init__(self) -> None:
        self.name = ""
        self.type = ""
        self.progress = 0
        self.total = 0
        self.complete = False


    def update(self, char: CharInfo) -> None:
        self.name = char.task
        self.type = char.task_type
        self.progress = char.task_progress
        self.total = char.task_total
        self.complete = self.total <= self.progress


class Inventory:
    def __init__(self):
        self.fill = 0.0
        self.maxSlots = 0
        self.usedSlots = 0
        self.freeSlots = 0
        self._items: list[InvInfo] = []


    def update(self, items: list[InvInfo], maxSlots: int) -> None:
        self._items = items
        self.maxSlots = maxSlots
        self.usedSlots = 0
        for item in self._items:
            if type(item) is not InvInfo:
                logger.error("Invalid item in inventory")
                continue
            self.usedSlots += item.quantity
        try:
            self.fill = self.usedSlots / self.maxSlots
        except ZeroDivisionError:
            self.fill = 1.0
        self.freeSlots = self.maxSlots - self.usedSlots


    def get(self, code: str) -> Union[InvInfo, None]:
        if code is None or code == "":
            return None
        for item in self._items:
            if item.code == code:
                return item
        return None
