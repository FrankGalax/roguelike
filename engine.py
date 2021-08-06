from typing import Iterable, Any, Optional

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from gamemap import GameMap
from inputhandlers import EventHandler
from statemachine import StateMachine, State
from procgen import generateDungeon
from actions import Action
from ui import UI


class GameState(State):
    def __init__(self, player: Entity, engine):
        super().__init__(player)
        self.player = player
        self.engine = engine

    def handleEvents(self, events: Iterable[Any]):
        for event in events:
            action = self.engine.eventHandler.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.onPlayerAction()

    def onPlayerAction(self):
        pass


class DungeonGameState(GameState):
    def __init__(self, player: Entity, engine):
        super().__init__(player, engine)
        self.gameMap: Optional[GameMap] = None
        self.ui = UI(player)

    def enter(self):
        mapWidth = 80
        mapHeight = 45

        roomMaxSize = 10
        roomMinSize = 6
        maxRooms = 30
        maxMonstersPerRoom = 2

        self.gameMap = generateDungeon(
            maxRooms=maxRooms,
            roomMinSize=roomMinSize,
            roomMaxSize=roomMaxSize,
            mapWidth=mapWidth,
            mapHeight=mapHeight,
            maxMonstersPerRoom=maxMonstersPerRoom,
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

    def render(self, console: Console, context: Context):
        self.gameMap.render(console)
        self.ui.renderHealthBar(console, totalWidth=20)

        context.present(console)
        console.clear()


class DeadPlayerGameState(GameState):
    def render(self, console: Console, context: Context):
        context.present(console)
        console.clear()


class Engine:
    def __init__(self, eventHandler: EventHandler, player: Entity):
        self.eventHandler = eventHandler
        self.player = player
        self.stateMachine = StateMachine(DungeonGameState(self.player, self))

    def handleEvents(self, events: Iterable[Any]) -> None:
        self.stateMachine.handleEvents(events)

    def render(self, console: Console, context: Context) -> None:
        self.stateMachine.render(console, context)
