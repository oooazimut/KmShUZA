from typing import Dict, List, Protocol


class Receiver(Protocol):
    async def receive(self) -> Dict[str, List]: ...
