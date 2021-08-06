from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from gamemap import GameMap
from inputhandlers import EventHandler


class Engine:
    def __init__(self, eventHandler: EventHandler, gameMap: GameMap, player: Entity):
        self.eventHandler = eventHandler
        self.gameMap = gameMap
        self.player = player
        self.updateFov()

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.handleEnemiesTurn()
            self.updateFov()

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

    def render(self, console: Console, context: Context) -> None:
        self.gameMap.render(console)

        context.present(console)

        console.clear()
