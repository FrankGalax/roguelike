from entity import Entity

class Component:
    def __init__(self):
        self.owner = None

    def setOwner(self, owner: Entity):
        self.owner = owner
        self.onOwnerChanged()

    def onOwnerChanged(self):
        pass
