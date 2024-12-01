from dataclasses import dataclass


@dataclass
class InvInfo:
    slot: int
    code: str
    quantity: int


@dataclass
class CharInfo:
    name: str
    account: str
    skin: str
    level: int
    xp: int
    max_xp: int
    gold: int
    speed: int
    mining_level: int
    mining_xp: int
    mining_max_xp: int
    woodcutting_level: int
    woodcutting_xp: int
    woodcutting_max_xp: int
    fishing_level: int
    fishing_xp: int
    fishing_max_xp: int
    weaponcrafting_level: int
    weaponcrafting_xp: int
    weaponcrafting_max_xp: int
    gearcrafting_level: int
    gearcrafting_xp: int
    gearcrafting_max_xp: int
    jewelrycrafting_level: int
    jewelrycrafting_xp: int
    jewelrycrafting_max_xp: int
    cooking_level: int
    cooking_xp: int
    cooking_max_xp: int
    alchemy_level: int
    alchemy_xp: int
    alchemy_max_xp: int
    hp: int
    max_hp: int
    haste: int
    critical_strike: int
    stamina: int
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    dmg_fire: int
    dmg_earth: int
    dmg_water: int
    dmg_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    x: int
    y: int
    cooldown: int
    cooldown_expiration: str
    weapon_slot: str
    shield_slot: str
    helmet_slot: str
    body_armor_slot: str
    leg_armor_slot: str
    boots_slot: str
    ring1_slot: str
    ring2_slot: str
    amulet_slot: str
    artifact1_slot: str
    artifact2_slot: str
    artifact3_slot: str
    utility1_slot: str
    utility1_slot_quantity: int
    utility2_slot: str
    utility2_slot_quantity: int
    task: str
    task_type: str
    task_progress: int
    task_total: int
    inventory_max_items: int
    inventory: list[InvInfo]


@dataclass
class Priorities:
    mining: float
    woodcutting: float
    fishing: float
    weaponcrafting: float
    gearcrafting: float
    jewelrycrafting: float
    cooking: float
    alchemy: float


@dataclass
class JobInfo:
    name: str
    id: int
    priorities: Priorities


@dataclass
class SkillInfo:
    name: str
    level: int
    maxLevel: int
    xp: int
    maxXp: int
    xpToLevel: int
    progress: float


@dataclass
class StateInfo:
    state: str
    target: tuple[int, int]
    code: str = ""
    amount: int = 0
