from typing import Any, Callable, Dict, List

from domain.models import Pump, Uza


def convert_to_bin(src: int, quantity: int) -> List[int]:
    return [int(b) for b in f"{src:0{quantity}b}"[::-1]]


def determine_models_values(registers, to_float_converter: Callable) -> Dict[str, Any]:
    return dict(
        selectors=registers[:3] + [registers[17]],
        permsissions=convert_to_bin(registers[3], 4),
        pump_conditions=convert_to_bin(registers[4], 3),
        uza_conditions=convert_to_bin(registers[5], 4),
        pressures=to_float_converter(registers[8:14]),
        pump_runtimes=registers[14:17],
    )


def convert_to_domain_models(
    registers: List, to_float_converter: Callable
) -> Dict[str, List[Any]]:
    values = determine_models_values(registers, to_float_converter)
    return {
        "pumps": construct_pumps(
            values["pump_conditions"], values["pressures"], values["pump_runtimes"]
        ),
        "uzas": construct_uzas(
            values["uza_conditions"], values["selectors"], values["permsissions"]
        ),
    }


def construct_pumps(
    conditions: List[int],
    pressures: List[float],
    runtimes: List[int],
    quantity: int = 3,
) -> List[Pump]:
    pumps = [
        Pump(
            name=str(num + 1),
            is_working=bool(conditions[num]),
            pressure=pressures[num],
            runtime=runtimes[num],
        )
        for num in range(quantity)
    ]
    pumps.sort(key=lambda x: x.name)
    return pumps


def construct_uzas(
    conditions: List[int],
    selectors: List[int],
    permissions: List[int],
    quantity: int = 4,
) -> List[Uza]:
    uzas = [
        Uza(
            number=num + 1,
            is_active=bool(conditions[num]),
            selector=selectors[num],
            permission=bool(permissions[num]),
        )
        for num in range(quantity)
    ]
    uzas.sort(key=lambda x: x.number)
    return uzas


def cache_data(func):
    async def wrapper(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)
        self._cache = result
        return result

    return wrapper
