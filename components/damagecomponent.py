from components.component import Component
from entity import RenderOrder


class DamageComponent(Component):
    def __init__(self, maxHp: int, armor: int):
        super().__init__()
        self.maxHp = maxHp
        self.currentHp = maxHp
        self.armor = armor
        self.isAlive = True

    def onOwnerChanged(self):
        self.owner.damageComponent = self

    def takeDamage(self, damage: int):
        if not self.isAlive:
            return

        damage -= self.armor

        if damage <= 0:
            return

        self.currentHp = max(self.currentHp - damage, 0)

        if self.currentHp == 0:
            self.die()

    def die(self):
        self.owner.char = "%"
        self.owner.color = (191, 0, 0)
        self.owner.blocksMovement = False
        self.owner.name = f"Remains of {self.owner.name}"
        self.owner.renderOrder = RenderOrder.Corpse
        self.isAlive = False
