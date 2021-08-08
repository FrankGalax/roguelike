import copy

from entity import Entity, RenderOrder
from components.damagecomponent import DamageComponent
from components.meleecomponent import MeleeComponent
from components.pathcomponent import PathComponent
from components.aicomponent import MeleeHostileAIComponent
from components.pickupablecomponent import PickupableComponent
from components.inventorycomponent import InventoryComponent
from components.itemcomponent import ItemComponent, HealItemEffect, LightningStrikeItemEffect, ConfuseItemEffect, \
                                     FireballItemEffect
from components.requestgamestatecomponent import RequestGameStateComponent
from gamemap import GameMap

player = Entity(char="@", color=(255, 255, 255), name="Player", blocksMovement=True, renderOrder=RenderOrder.Actor)
player.addComponent(DamageComponent(10, 1))
player.addComponent(MeleeComponent(2))
player.addComponent(InventoryComponent(10))
player.addComponent(RequestGameStateComponent())

orc = Entity(char="o", color=(63, 127, 63), name="Orc", blocksMovement=True, renderOrder=RenderOrder.Actor)
orc.addComponent(DamageComponent(4, 0))
orc.addComponent(MeleeComponent(2))
orc.addComponent(PathComponent())
orc.addComponent(MeleeHostileAIComponent())

troll = Entity(char="T", color=(0, 127, 0), name="Troll", blocksMovement=True, renderOrder=RenderOrder.Actor)
troll.addComponent(DamageComponent(6, 1))
troll.addComponent(MeleeComponent(2))
troll.addComponent(PathComponent())
troll.addComponent(MeleeHostileAIComponent())

healthPotion = Entity(char="!", color=(127, 0, 255), name="Health Potion", blocksMovement=False,
                      renderOrder=RenderOrder.Item)
healthPotion.addComponent(PickupableComponent())
healthPotion.addComponent(ItemComponent([HealItemEffect(10)]))

lightningScroll = Entity(char="~", color=(255, 255, 0), name="Lightning Scroll", blocksMovement=False,
                         renderOrder=RenderOrder.Item)
lightningScroll.addComponent(PickupableComponent())
lightningScroll.addComponent(ItemComponent([LightningStrikeItemEffect(5)]))

confusionScroll = Entity(char="~", color=(207, 63, 255), name="Confusion Scroll", blocksMovement=False,
                         renderOrder=RenderOrder.Item)
confusionScroll.addComponent(PickupableComponent())
confusionScroll.addComponent(ItemComponent([ConfuseItemEffect(3)]))

fireballScroll = Entity(char="~", color=(255, 0, 0), name="Fireball Scroll", blocksMovement=False,
                        renderOrder=RenderOrder.Item)
fireballScroll.addComponent(PickupableComponent())
fireballScroll.addComponent(ItemComponent([FireballItemEffect(10, 3)]))


def spawnEntity(entity: Entity, gameMap: GameMap, x: int, y: int) -> Entity:
    clone = copy.deepcopy(entity)
    clone.x = x
    clone.y = y
    gameMap.entities.add(clone)
    clone.setGameMap(gameMap)
    for component in clone.components:
        component.onAddToGameMap(gameMap)
    return clone
