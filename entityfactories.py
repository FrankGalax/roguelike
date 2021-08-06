import copy

from entity import Entity, RenderOrder
from components.damagecomponent import DamageComponent
from components.meleecomponent import MeleeComponent
from components.pathcomponent import PathComponent
from components.aicomponent import MeleeHostileAIComponent
from gamemap import GameMap

player = Entity(char="@", color=(255, 255, 255), name="Player", blocksMovement=True, renderOrder=RenderOrder.Actor)
player.addComponent(DamageComponent(10, 2))
player.addComponent(MeleeComponent(2))

orc = Entity(char="o", color=(63, 127, 63), name="Orc", blocksMovement=True, renderOrder=RenderOrder.Actor)
orc.addComponent(DamageComponent(4, 0))
orc.addComponent(MeleeComponent(1))
orc.addComponent(PathComponent())
orc.addComponent(MeleeHostileAIComponent())

troll = Entity(char="T", color=(0, 127, 0), name="Troll", blocksMovement=True, renderOrder=RenderOrder.Actor)
troll.addComponent(DamageComponent(8, 1))
troll.addComponent(MeleeComponent(2))
troll.addComponent(PathComponent())
troll.addComponent(MeleeHostileAIComponent())


def spawnEntity(entity: Entity, gameMap: GameMap, x: int, y: int) -> Entity:
    clone = copy.deepcopy(entity)
    clone.x = x
    clone.y = y
    gameMap.entities.add(clone)
    clone.setGameMap(gameMap)
    for component in clone.components:
        component.onAddToGameMap(gameMap)
    return clone
