from typing import Optional, Tuple

import color
from entity import Entity


class Action:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.success = False

    def perform(self) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def destXY(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blockingEntity(self) -> Optional[Entity]:
        return self.entity.gameMap.getBlockingEntityAtLocation(*self.destXY)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blockingEntity

        if not target:
            self.entity.gameMap.messageLog.addMessage("Nothing to attack.", color.impossible)
            return

        if not target.damageComponent:
            return

        if not self.entity.meleeComponent:
            return

        target.damageComponent.takeDamage(self.entity, self.entity.meleeComponent.attack)
        self.success = True


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        gameMap = self.entity.gameMap
        if not gameMap.inBounds(destX, destY):
            self.entity.gameMap.messageLog.addMessage("That way is blocked.", color.impossible)
            return
        if not gameMap.tiles["walkable"][destX, destY]:
            self.entity.gameMap.messageLog.addMessage("That way is blocked.", color.impossible)
            return
        if gameMap.getBlockingEntityAtLocation(destX, destY):
            self.entity.gameMap.messageLog.addMessage("That way is blocked.", color.impossible)
            return

        self.entity.move(self.dx, self.dy)
        self.success = True


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        gameMap = self.entity.gameMap
        if gameMap.getBlockingEntityAtLocation(destX, destY):
            meleeAction = MeleeAction(self.entity, self.dx, self.dy)
            meleeAction.perform()
            self.success = meleeAction.success
            return

        movementAction = MovementAction(self.entity, self.dx, self.dy)
        movementAction.perform()
        self.success = movementAction.success


class PickupAction(Action):
    def perform(self) -> None:
        destX, destY = self.entity.x, self.entity.y

        gameMap = self.entity.gameMap
        entity = gameMap.getEntityAtLocation(destX, destY, allowPlayer=False)

        if not entity:
            self.entity.gameMap.messageLog.addMessage("Nothing to use", color.impossible)
            return

        if not entity.pickupableComponent:
            self.entity.gameMap.messageLog.addMessage(f"{entity.name} is not pickupable", color.impossible)
            return

        if not self.entity.inventoryComponent:
            self.entity.gameMap.messageLog.addMessage(f"{self.entity.name} cannot pickup items", color.impossible)
            return

        inventory = self.entity.inventoryComponent

        if len(inventory.items) == inventory.maxItems:
            self.entity.gameMap.messageLog.addMessage("Inventory is full", color.impossible)
            return

        entity.pickupableComponent.pickup(self.entity)
        self.success = True


class UseItemAction(Action):
    def __init__(self, entity: Entity, itemIndex: int):
        super().__init__(entity)
        self.itemIndex = itemIndex

    def perform(self) -> None:
        items = self.entity.inventoryComponent.items

        if self.itemIndex >= len(items):
            if self.itemIndex == 0:
                slotNumberStr = "1st"
            elif self.itemIndex == 1:
                slotNumberStr = "2nd"
            elif self.itemIndex == 2:
                slotNumberStr = "3rd"
            else:
                slotNumberStr = f"{self.itemIndex + 1}th"

            self.entity.gameMap.messageLog.addMessage(f"No item is present in the {slotNumberStr} inventory slot",
                                                      color.impossible)
            return

        item = items[self.itemIndex]
        self.entity.gameMap.messageLog.addMessage(f"{self.entity.name} used the {item.name}", color.itemPickedUp)
        item.itemComponent.apply(self.entity)
        self.entity.inventoryComponent.items.remove(item)

        if self.entity.requestGameStateComponent and self.entity.requestGameStateComponent.requestedGameState:
            return

        self.success = True
