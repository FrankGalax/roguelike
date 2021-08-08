from components.component import Component
from entity import Entity, RenderOrder
from signal import Signal
import color


class DamageComponent(Component):
    def __init__(self, maxHp: int, armor: int):
        super().__init__()
        self.maxHp = maxHp
        self.currentHp = maxHp
        self.armor = armor
        self.isAlive = True
        self.signalCurrentHpChanged = Signal()
        self.signalDie = Signal()

    def onOwnerChanged(self):
        self.owner.damageComponent = self

    def takeDamage(self, instigator: Entity, damage: int):
        if not self.isAlive:
            return

        damage -= self.armor

        if damage < 0:
            damage = 0

        attackDesc = f"{instigator.name.capitalize()} attacks {self.owner.name}"
        attackColor = color.enemyAtk
        if self.owner.isPlayer:
            attackColor = color.playerAtk

        if damage > 0:
            self.owner.gameMap.messageLog.addMessage(f"{attackDesc} for {damage} hit points", attackColor)

            self.currentHp = max(self.currentHp - damage, 0)
            self.signalCurrentHpChanged.signal1(self.currentHp)

            if self.currentHp == 0:
                self.die()
        else:
            self.owner.gameMap.messageLog.addMessage(f"{attackDesc} but does no damage")

    def heal(self, amount: int):
        if amount > self.maxHp - self.currentHp:
            amount = self.maxHp - self.currentHp

        self.currentHp += amount

        if amount == 0:
            self.owner.gameMap.messageLog.addMessage(f"{self.owner.name} is already at maximum hit points", color.healthRecovered)
        else:
            self.owner.gameMap.messageLog.addMessage(f"{self.owner.name} heals for {amount} hit points", color.healthRecovered)

        self.signalCurrentHpChanged.signal1(self.currentHp)

    def die(self):
        deathMessage = f"{self.owner.name} is dead!"
        deathMessageColor = color.enemyDie

        if self.owner.isPlayer:
            deathMessage = f"You died!"
            deathMessageColor = color.playerDie

        self.owner.char = "%"
        self.owner.color = (191, 0, 0)
        self.owner.blocksMovement = False
        self.owner.name = f"Remains of {self.owner.name}"
        self.owner.renderOrder = RenderOrder.Corpse
        self.isAlive = False
        self.signalDie.signal0()

        self.owner.gameMap.messageLog.addMessage(deathMessage, deathMessageColor)
