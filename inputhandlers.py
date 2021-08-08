from typing import Optional

import tcod.event
from entity import Entity
from actions import Action, EscapeAction, BumpAction, PickupAction, UseItemAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, player: Entity):
        self.player = player
        self.mouseLocation = (0, 0)


class DungeonEventHandler(EventHandler):
    def __init__(self, player: Entity):
        super().__init__(player)
        self.viewInventoryRequested = False

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP or key == tcod.event.K_w:
            action = BumpAction(self.player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN or key == tcod.event.K_s:
            action = BumpAction(self.player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT or key == tcod.event.K_a:
            action = BumpAction(self.player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT or key == tcod.event.K_d:
            action = BumpAction(self.player, dx=1, dy=0)
        elif key == tcod.event.K_e:
            action = PickupAction(self.player)
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(self.player)
        elif key == tcod.event.K_i:
            self.viewInventoryRequested = True

        return action

    def ev_mousemotion(self, event: tcod.event.MouseMotion):
        if self.player:
            if self.player.gameMap:
                if self.player.gameMap.inBounds(event.tile.x, event.tile.y):
                    self.mouseLocation = event.tile.x, event.tile.y


class ViewInventoryEventHandler(EventHandler):
    def __init__(self, player: Entity):
        super().__init__(player)
        self.exitViewInventoryRequested = False

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_1:
            action = UseItemAction(self.player, 0)
        elif key == tcod.event.K_2:
            action = UseItemAction(self.player, 1)
        elif key == tcod.event.K_3:
            action = UseItemAction(self.player, 2)
        elif key == tcod.event.K_4:
            action = UseItemAction(self.player, 3)
        elif key == tcod.event.K_5:
            action = UseItemAction(self.player, 4)
        elif key == tcod.event.K_6:
            action = UseItemAction(self.player, 5)
        elif key == tcod.event.K_7:
            action = UseItemAction(self.player, 6)
        elif key == tcod.event.K_8:
            action = UseItemAction(self.player, 7)
        elif key == tcod.event.K_9:
            action = UseItemAction(self.player, 8)
        elif key == tcod.event.K_0:
            action = UseItemAction(self.player, 9)
        elif key == tcod.event.K_i:
            self.exitViewInventoryRequested = True

        return action


class TargetEventHandler(EventHandler):
    def __init__(self, player: Entity):
        super().__init__(player)
        self.mouseLocation = (player.x, player.y)
        self.targetSelected = False

    def ev_mousemotion(self, event: tcod.event.MouseMotion):
        if self.player:
            if self.player.gameMap:
                if self.player.gameMap.inBounds(event.tile.x, event.tile.y):
                    if self.player.gameMap.visible[event.tile.x, event.tile.y]:
                        self.mouseLocation = event.tile.x, event.tile.y

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        if self.player.gameMap.inBounds(*event.tile):
            if event.button == 1:
                self.targetSelected = True
