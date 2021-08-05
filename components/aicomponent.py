from typing import Optional
from components.component import Component
from entity import Entity
from gamemap import GameMap
from actions import Action
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
        """
        if self.gameMap.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return None

            self.path = self.get_path_to(target.x, target.y)
            self.

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()
        """
        return None

class AIComponent(Component):
    def __init__(self, player: Entity):
        super().__init__()
        self.player = player

    def getAction(self, gameMap: GameMap) -> Action:
        raise NotImplementedError()

    def onOwnerChanged(self):
        self.owner.aiComponent = self


class MeleeHostileAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.stateMachine = StateMachine()
