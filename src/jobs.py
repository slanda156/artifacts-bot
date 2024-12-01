from src.dataclasses import JobInfo, Priorities


_priorities = Priorities(0, 0, 0, 0, 0, 0, 0, 0)
FIGHTER = JobInfo("Fighter", 1, _priorities)

_priorities = Priorities(0.5, 0.5, 0, 0, 0, 0, 0, 0)
GATHERER = JobInfo("Gatherer", 2, _priorities)

_priorities = Priorities(0, 0, 0, 0.6, 0.4, 0, 0, 0)
SMITH = JobInfo("Smith", 3, _priorities)

_priorities = Priorities(0, 0, 0.4, 0, 0, 0, 0.6, 0)
COOK = JobInfo("Cook", 4, _priorities)

_priorities = Priorities(0, 0, 0, 0, 0, 0.6, 0, 0.4)
ALCHEMIST = JobInfo("Alchemist", 5, _priorities)


CHARACTERJOBMAP = {
    "gawin": FIGHTER
}
