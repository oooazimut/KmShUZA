from typing import Protocol


class Receiver(Protocol):
    def get_data(self):
        pass


class Repo(Protocol):
    def save_data(self):
        pass
