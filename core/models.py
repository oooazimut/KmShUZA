from dataclasses import dataclass


@dataclass
class Pump:
    is_working: bool
    pressure: float
    work: int


@dataclass
class Uza:
    is_active: bool
