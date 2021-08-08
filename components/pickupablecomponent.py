import color
from components.component import Component
from entity import Entity


class PickupableComponent(Component):
    def onOwnerChanged(self):
        self.owner.pickupableComponent = self

    def pickup(self, instigator: Entity):
        if not instigator:
            return

        if not instigator.inventoryComponent:
            return

        self.owner.gameMap.removeEntity(self.owner)
        instigator.inventoryComponent.addItem(self.owner)
        instigator.gameMap.messageLog.addMessage(f"{instigator.name} picked up {self.owner.name}", color.itemPickedUp)
