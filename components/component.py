from entity import Entity
from gamemap import GameMap

class Component:
    def __init__(self):
        self.owner = None

    def setOwner(self, owner: Entity):
        self.owner = owner
        self.onOwnerChanged()

    def onOwnerChanged(self):
        pass

    def onAddToGameMap(self, gameMap: GameMap):
        pass
