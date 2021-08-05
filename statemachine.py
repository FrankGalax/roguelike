from typing import Optional
from actions import Action
from entity import Entity

class State:
    def __init__(self, entity: Entity):
        self.entity = entity

    def enter(self):
        pass

    def exit(self):
        pass

    def getAction(self) -> Optional[Action]:
        raise NotImplementedError()


class StateMachine:
    def __init__(self, state: Optional[State]):
        self.state: Optional[State] = state

    def transition(self, state: State):
        if self.state:
            self.state.exit()

        self.state = state

        if self.state:
            self.state.enter()

    def getAction(self) -> Optional[Action]:
        if self.state:
            return self.state.getAction()

        return None
