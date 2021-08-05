from __future__ import annotations

from typing import Optional, Tuple

from entity import Entity
from gamemap import GameMap


class Action:
    def __init__(self, entity: Entity, gameMap: GameMap) -> None:
        self.entity = entity
        self.gameMap = gameMap

    def perform(self) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, gameMap: GameMap, dx: int, dy: int):
        super().__init__(entity, gameMap)
        self.dx = dx
        self.dy = dy

    @property
    def destXY(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blockingEntity(self) -> Optional[Entity]:
        return self.gameMap.getBlockingEntityAtLocation(*self.destXY)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blockingEntity

        if not target:
            return

        if not target.damageComponent:
            return

        if not self.entity.meleeComponent:
            return

        target.damageComponent.takeDamage(self.entity.meleeComponent.attack)


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        if not self.gameMap.inBounds(destX, destY):
            return
        if not self.gameMap.tiles["walkable"][destX, destY]:
            return
        if self.gameMap.getBlockingEntityAtLocation(destX, destY):
            return

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        if self.gameMap.getBlockingEntityAtLocation(destX, destY):
            return MeleeAction(self.entity, self.gameMap, self.dx, self.dy).perform()

        return MovementAction(self.entity, self.gameMap, self.dx, self.dy).perform()
