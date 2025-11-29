from typing import (
    Any,
    Callable,
    Dict,
    List,
    Type,
    TypeVar,
)

from domain.models import Pump, Uza


def convert_to_bool(src: int, quantity: int) -> List[bool]:
    return [bool(int(b)) for b in f"{src:0{quantity}b}"[::-1]]


def determine_uza_values(registers, q: int = 4) -> Dict[str, List]:
    return {
        "number": [i + 1 for i in range(q)],
        "selector": registers[:3] + [registers[17]],
        "permission": convert_to_bool(registers[3], q),
        "is_active": convert_to_bool(registers[5], q),
        "break_alert": convert_to_bool(registers[6], 4),
    }


def determine_pump_values(
    registers, to_float_converter: Callable, q: int = 3
) -> Dict[str, List]:
    return {
        "name": [str(i + 1) for i in range(q)],
        "is_working": list(
            map(lambda x: round(x, 2), (convert_to_bool(registers[4], q)))
        ),
        "pressure": to_float_converter(registers[8:14]),
        "runtime": registers[14:17],
        "emergency_mode": convert_to_bool(registers[18], q),
        "pressure_alert": convert_to_bool(registers[19], q),
    }


def convert_to_domain_models(
    registers: List, to_float_converter: Callable
) -> Dict[str, List]:
    return {
        "pumps": construct_pumps(determine_pump_values(registers, to_float_converter)),
        "uzas": construct_uzas(determine_uza_values(registers)),
    }


def construct_pumps(data: Dict, quantity: int = 3) -> List[Pump]:
    return construct_items(Pump, data, quantity)


def construct_uzas(data: Dict, quantity: int = 4) -> List[Uza]:
    return construct_items(Uza, data, quantity)


T = TypeVar("T")


def construct_items(
    model: Type[T], data: Dict[str, List[Any]], quantity: int
) -> List[T]:
    return [model(**{key: data[key][num] for key in data}) for num in range(quantity)]
