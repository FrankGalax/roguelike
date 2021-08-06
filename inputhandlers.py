from typing import Optional

import tcod.event
from entity import Entity
from gamemap import GameMap
from actions import Action, EscapeAction, BumpAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, player: Entity):
        self.player = player

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(self.player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(self.player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(self.player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(self.player, dx=1, dy=0)
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(self.player)

        return action
