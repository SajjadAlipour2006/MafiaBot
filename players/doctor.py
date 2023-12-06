from .villager import VillagerPlayer
from .protector import ProtectorPlayer


class DoctorPlayer(VillagerPlayer, ProtectorPlayer):
    protecting_power = 1
