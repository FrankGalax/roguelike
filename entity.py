from typing import Tuple
from enum import auto, Enum


class RenderOrder(Enum):
    Corpse = auto()
    Item = auto()
    Actor = auto()


class Entity:
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocksMovement: bool = False,
        renderOrder: RenderOrder = RenderOrder.Actor
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocksMovement = blocksMovement
        self.components = []
        self.damageComponent = None
        self.meleeComponent = None
        self.pathComponent = None
        self.aiComponent = None
        self.renderOrder = renderOrder

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def addComponent(self, component):
        component.setOwner(self)
        self.components.append(component)