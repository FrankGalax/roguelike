from typing import List
from components.component import Component
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


class ItemComponent(Component):
    def __init__(self, itemEffects: List[ItemEffect]):
        super().__init__()
        self.itemEffects = itemEffects

    def onOwnerChanged(self):
        self.owner.itemComponent = self

    def apply(self, entity: Entity):
        for itemEffect in self.itemEffects:
            itemEffect.apply(entity)
