from typing import Iterable, Any, Optional, Tuple

import tcod
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from gamemap import GameMap
from inputhandlers import EventHandler, DungeonEventHandler, ViewInventoryEventHandler
from statemachine import StateMachine, State
from procgen import generateDungeon
from actions import Action
from ui import UI


class GameState(State):
    def __init__(self, player: Entity, engine):
        super().__init__(player)
        self.player = player
        self.engine = engine

    def handleEvents(self, events: Iterable[Any], context: tcod.context.Context):
        if self.engine.eventHandler:
            for event in events:
                context.convert_event(event)
                action = self.engine.eventHandler.dispatch(event)

                if action is None:
                    continue

                action.perform()
                if action.success:
                    self.onPlayerAction()

            self.onHandleEvents()

    def onPlayerAction(self):
        pass


class IdleDungeonGameState(State):
    def __init__(self, player: Entity, engine):
        super().__init__(player)
        self.engine = engine

    def enter(self):
        self.engine.eventHandler = DungeonEventHandler(self.entity)

    def onHandleEvents(self):
        if self.engine.eventHandler.viewInventoryRequested:
            self.engine.eventHandler.viewInventoryRequested = False
            self.transition(ViewingInventoryGameState(self.entity, self.engine))


class ViewingInventoryGameState(State):
    def __init__(self, player: Entity, engine):
        super().__init__(player)
        self.engine = engine

    def enter(self):
        self.engine.eventHandler = ViewInventoryEventHandler(self.entity)

    def onHandleEvents(self):
        if self.engine.eventHandler.exitViewInventoryRequested:
            self.engine.eventHandler.exitViewInventoryRequested = False
            self.transition(IdleDungeonGameState(self.entity, self.engine))

    def render(self, console, context):
        nbInventoryItems = len(self.entity.inventoryComponent.items)
        height = nbInventoryItems + 2

        if height <= 3:
            height = 3

        if self.entity.x <= 30:
            x = 40
        else:
            x = 0
        y = 0

        title = "Inventory"
        width = 25

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=title,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if nbInventoryItems > 0:
            for i, item in enumerate(self.entity.inventoryComponent.items):
                console.print(x + 1, y + i + 1, f"({i + 1}) {item.name}")
        else:
            console.print(x + 1, y + 1, "(Empty)")


class DungeonGameState(GameState):
    def __init__(self, player: Entity, engine):
        super().__init__(player, engine)
        self.gameMap: Optional[GameMap] = None
        self.ui = UI(player)
        self.stateMachine = StateMachine(IdleDungeonGameState(self.player, self.engine))

    def enter(self):
        mapWidth = 80
        mapHeight = 45

        roomMaxSize = 10
        roomMinSize = 6
        maxRooms = 30
        maxMonstersPerRoom = 2
        maxItemsPerRoom = 2

        self.gameMap = generateDungeon(
            maxRooms=maxRooms,
            roomMinSize=roomMinSize,
            roomMaxSize=roomMaxSize,
            mapWidth=mapWidth,
            mapHeight=mapHeight,
            maxMonstersPerRoom=maxMonstersPerRoom,
            maxItemsPerRoom=maxItemsPerRoom,
            player=self.player
        )
        self.player.setGameMap(self.gameMap)

        self.updateFov()

    def getAction(self) -> Optional[Action]:
        return None

    def onPlayerAction(self):
        self.handleEnemiesTurn()
        self.updateFov()

        if not self.player.damageComponent.isAlive:
            self.engine.stateMachine.transition(DeadPlayerGameState(self.player, self.engine))

    def onHandleEvents(self):
        self.stateMachine.onHandleEvents()

    def handleEnemiesTurn(self):
        for enemy in self.gameMap.entities - {self.player}:
            if enemy.aiComponent:
                action = enemy.aiComponent.getAction()
                if action:
                    action.perform()

    def updateFov(self) -> None:
        self.gameMap.visible[:] = compute_fov(
            self.gameMap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.gameMap.explored |= self.gameMap.visible

    def renderNamesAtLocation(self, console: tcod.Console, x: int, y: int, location: Tuple[int, int]):
        if not self.gameMap.inBounds(location[0], location[1]) or not self.gameMap.visible[location[0], location[1]]:
            return

        names = ", ".join(entity.name for entity in self.gameMap.entities if entity.x == location[0] and entity.y == location[1])
        console.print(x=x, y=y, string=names)

    def render(self, console: Console, context: Context):
        self.gameMap.render(console)
        self.ui.renderHealthBar(console, totalWidth=20)
        self.renderNamesAtLocation(console, 21, 44, self.engine.eventHandler.mouseLocation)

        self.stateMachine.render(console, context)

        context.present(console)
        console.clear()


class DeadPlayerGameState(GameState):
    def render(self, console: Console, context: Context):
        context.present(console)
        console.clear()


class Engine:
    def __init__(self, player: Entity):
        self.eventHandler: Optional[EventHandler] = None
        self.player = player
        self.stateMachine = StateMachine(DungeonGameState(self.player, self))

    def handleEvents(self, events: Iterable[Any], context: tcod.context.Context) -> None:
        self.stateMachine.handleEvents(events, context)

    def render(self, console: Console, context: Context) -> None:
        self.stateMachine.render(console, context)
