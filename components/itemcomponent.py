from typing import List

import color
from components.component import Component
from components.requestgamestatecomponent import GameStateRequest
from entity import Entity


class ItemEffect:
    def apply(self, entity: Entity):
        raise NotImplementedError()


class HealItemEffect(ItemEffect):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, entity: Entity):
        if not entity.damageComponent:
            entity.gameMap.messageLog.addMessage("Item does nothing...")
            return

        entity.damageComponent.heal(self.amount)


class LightningStrikeItemEffect(ItemEffect):
    def __init__(self, damage: int):
        self.damage = damage

    def apply(self, entity: Entity):
        closestEntity = None
        closestDistance = 100

        for otherEntity in entity.gameMap.entities:
            if otherEntity is entity:
                continue

            if not entity.gameMap.visible[otherEntity.x, otherEntity.y]:
                continue

            if not entity.damageComponent:
                continue

            distance = otherEntity.distance(entity.x, entity.y)
            if distance < closestDistance:
                closestEntity = otherEntity
                closestDistance = distance

        if not closestEntity:
            entity.gameMap.messageLog.addMessage(f"The lightning strike didn't hit anything", color.impossible)

        entity.gameMap.messageLog.addMessage(
            f"A lighting bolt strikes the {closestEntity.name} with a loud thunder, for {self.damage} damage!")
        closestEntity.damageComponent.takeDamage(entity, self.damage)


class ConfuseItemEffect(ItemEffect):
    def __init__(self, nbTurns: int):
        self.nbTurns = nbTurns

    def apply(self, entity: Entity):
        if not entity.requestGameStateComponent:
            return

        entity.requestGameStateComponent.requestedGameState = GameStateRequest(
            "SingleRangeTargetState", int1=0, callback=lambda x: self.activate(x))

    def activate(self, entity: Entity):
        if not entity:
            return

        if not entity.aiComponent:
            entity.gameMap.messageLog.addMessage(f"{entity.name} cannot be confused!", color.impossible)

        entity.gameMap.messageLog.addMessage(
            f"The eyes of the {entity.name} look vacant, as it starts to stumble around!",
            color.statusEffectApplied,
        )
        entity.aiComponent.confuse(self.nbTurns)


class FireballItemEffect(ItemEffect):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def apply(self, entity: Entity):
        if not entity.requestGameStateComponent:
            return

        entity.requestGameStateComponent.requestedGameState = GameStateRequest(
            "AreaRangeTargetState", int1=self.radius, callback=lambda x, y: self.activate(x, y, entity)
        )

    def activate(self, x: int, y: int, entity: Entity):
        entity.gameMap.messageLog.addMessage("An immense fireball explodes in the area", color.red)
        for otherEntity in entity.gameMap.entities:
            if not entity.gameMap.visible[otherEntity.x, otherEntity.y]:
                continue

            if otherEntity is entity:
                continue

            if abs(otherEntity.x - x) > self.radius or abs(otherEntity.y - y) > self.radius:
                continue

            if not otherEntity.damageComponent:
                continue

            otherEntity.damageComponent.takeDamage(entity, self.damage)


class ItemComponent(Component):
    def __init__(self, itemEffects: List[ItemEffect]):
        super().__init__()
        self.itemEffects = itemEffects

    def onOwnerChanged(self):
        self.owner.itemComponent = self

    def apply(self, entity: Entity):
        for itemEffect in self.itemEffects:
            itemEffect.apply(entity)
