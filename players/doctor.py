from .villager import Villager
from .protector import Protector


class Doctor(Villager, Protector):
    protecting_power = 1
