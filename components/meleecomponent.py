from components.component import Component


class MeleeComponent(Component):
    def __init__(self, attack: int):
        self.attack = attack

    def onOwnerChanged(self):
        self.owner.meleeComponent = self
