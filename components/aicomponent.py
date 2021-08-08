from typing import Optional
from components.component import Component
from entity import Entity
from gamemap import GameMap
from actions import Action, MovementAction, MeleeAction
from statemachine import StateMachine, State


class GoToPlayerState(State):
    def __init__(self, entity: Entity, player: Entity):
        super().__init__(entity)
        self.player = player

    def exit(self):
        self.entity.pathComponent.clearPath()

    def getAction(self) -> Optional[Action]:
        distanceX = self.player.x - self.entity.x
        distanceY = self.player.y - self.entity.y
        distance = max(abs(distanceX), abs(distanceY))

        if self.entity.gameMap.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, distanceX, distanceY)

            self.entity.pathComponent.setPathTo(self.player.x, self.player.y)

        if len(self.entity.pathComponent.path) > 0:
            destX, destY = self.entity.pathComponent.path.pop(0)
            return MovementAction(self.entity, destX - self.entity.x, destY - self.entity.y)

        return None


class DeadState(State):
    def getAction(self) -> Optional[Action]:
        return None


class AIComponent(Component):
    def __init__(self):
        super().__init__()

    def onOwnerChanged(self):
        self.owner.aiComponent = self

    def getAction(self) -> Optional[Action]:
        raise NotImplementedError()


class MeleeHostileAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.stateMachine: Optional[StateMachine] = None

    def onAddToGameMap(self, gameMap: GameMap):
        super().onAddToGameMap(gameMap)
        self.stateMachine = StateMachine(GoToPlayerState(self.owner, self.owner.gameMap.player))

        if self.owner.damageComponent:
            self.owner.damageComponent.signalDie.addSlot(lambda: self.stateMachine.transition(DeadState(self.owner)))

    def getAction(self) -> Optional[Action]:
        if self.stateMachine:
            return self.stateMachine.getAction()

        return None

