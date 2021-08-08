from typing import Optional
from components.component import Component
from entity import Entity
from gamemap import GameMap
from actions import Action, MovementAction, MeleeAction, BumpAction
from statemachine import StateMachine, State
import random


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


class ConfusionState(State):
    def __init__(self, entity: Entity, nbTurns: int):
        super().__init__(entity)
        self.nbTurns = nbTurns

    def getAction(self) -> Optional[Action]:
        directionX, directionX = random.choice(
            [
                (-1, -1),  # Northwest
                (0, -1),  # North
                (1, -1),  # Northeast
                (-1, 0),  # West
                (1, 0),  # East
                (-1, 1),  # Southwest
                (0, 1),  # South
                (1, 1),  # Southeast
            ]
        )

        self.nbTurns -= 1

        if self.nbTurns == 0:
            self.entity.gameMap.messageLog.addMessage(f"The {self.entity.name} is no longer confused.")
            self.transition(GoToPlayerState(self.entity, self.entity.gameMap.player))

        return BumpAction(self.entity, directionX, directionX)


class AIComponent(Component):
    def __init__(self):
        super().__init__()

    def onOwnerChanged(self):
        self.owner.aiComponent = self

    def getAction(self) -> Optional[Action]:
        raise NotImplementedError()

    def confuse(self, nbTurns: int):
        pass

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

    def confuse(self, nbTurns: int):
        self.stateMachine.transition(ConfusionState(self.owner, nbTurns))
