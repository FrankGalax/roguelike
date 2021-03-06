from typing import Iterable, Optional
import numpy as np
from tcod.console import Console

import tiletypes
from entity import Entity
from message import MessageLog
import color


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = (), player: Optional[Entity] = None):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tiletypes.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
        self.player = player
        self.messageLog = MessageLog()
        self.messageLog.addMessage("Hello and welcome, adventurer, to yet another dungeon!", color.welcomeText)

    def inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiletypes.SHROUD
        )

        sortedEntities = sorted(self.entities, key=lambda x: x.renderOrder.value)

        for entity in sortedEntities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        self.messageLog.render(console=console, x=21, y=45, width=50, height=5)

    def getBlockingEntityAtLocation(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocksMovement and entity.x == x and entity.y == y:
                return entity

        return None

    def getEntityAtLocation(self, x: int, y: int, allowPlayer: bool) -> Optional[Entity]:
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                if not entity.isPlayer or allowPlayer:
                    return entity

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)
