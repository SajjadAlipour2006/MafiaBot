from .villager import Villager
from .protector import Protector


class Doctor(Villager, Protector):
    emoji = "👨‍⚕️"
    protecting_power = 1
