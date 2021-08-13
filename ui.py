from entity import Entity
from tcod.console import Console
import color


class UI:
    def __init__(self, player: Entity):
        self.player = player
        self.playerCurrentHp: int = 0
        self.playerMaxHp: int = 0

        if self.player:
            if self.player.damageComponent:
                self.playerMaxHp = self.player.damageComponent.maxHp

                self.player.damageComponent.signalCurrentHpChanged.addSlot(lambda x: self.onPlayerCurrentHpChanged(x))
                self.onPlayerCurrentHpChanged(self.player.damageComponent.currentHp)

    def onPlayerCurrentHpChanged(self, currentHp: int):
        self.playerCurrentHp = currentHp

    def renderHealthBar(self, console: Console, totalWidth: int):
        bar_width = int(float(self.playerCurrentHp) / self.playerMaxHp * totalWidth)

        console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.barEmpty)

        if bar_width > 0:
            console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=color.barFilled)

        console.print(x=1, y=45, string=f"HP: {self.playerCurrentHp}/{self.playerMaxHp}", fg=color.barText)
