from typing import Optional
from components.component import Component


class GameStateRequest:
    def __init__(self, name: str, int1: int, callback):
        self.name = name
        self.int1 = int1
        self.callback = callback


class RequestGameStateComponent(Component):
    def __init__(self):
        super().__init__()
        self.requestedGameState: Optional[GameStateRequest] = None

    def onOwnerChanged(self):
        self.owner.requestGameStateComponent = self
