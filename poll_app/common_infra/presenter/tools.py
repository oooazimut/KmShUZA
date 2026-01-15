from collections import defaultdict
from typing import Dict
from typing_extensions import List

from domain.entities import Pump


def group_pumps_by_name(pumps: List[Pump]) -> Dict[str, List[Pump]]:
    grouped_pumps = defaultdict(list)
    for pump in pumps:
        grouped_pumps[pump.name].append(pump)

    return grouped_pumps
