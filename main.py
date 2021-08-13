#!/usr/bin/env python3
import tcod
import copy
from typing import Optional

from engine import Engine
import entityfactories
from statemachine import StateMachine, State
import color
from inputhandlers import MainMenuEventHandler


class MainMenuState(State):
    def __init__(self, player):
        super().__init__(player)
        self.backgroundImage = tcod.image.load("menu_background.png")[:, :, :3]
        self.eventHandler = MainMenuEventHandler(player)

    def render(self, console, context):
        console.draw_semigraphics(self.backgroundImage, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "ANOTHER ROGUELIKE",
            fg=color.menuTitle,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By (Galax and Anoex)",
            fg=color.menuTitle,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
                ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menuText,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

        context.present(console)
        console.clear()

        events = tcod.event.wait()

        for event in events:
            self.eventHandler.dispatch(event)

        if self.eventHandler.newGameRequested:
            self.eventHandler.newGameRequested = False
            self.transition(PlayState(self.entity, None))
        elif self.eventHandler.continueRequested:
            self.eventHandler.continueRequested = False
            self.transition(PlayState(self.entity, "savegame.sav"))


class PlayState(State):
    def __init__(self, player, saveFile=Optional[str]):
        super().__init__(player)
        self.engine = Engine(player=player, saveFile=saveFile)
        if saveFile:
            self.entity = self.engine.player

    def render(self, console: tcod.console.Console, context: tcod.context.Context):
        self.engine.render(console=console, context=context)
        events = tcod.event.wait()
        self.engine.handleEvents(events, context)

        if not self.entity.damageComponent.isAlive:
            self.transition(MainMenuState(copy.deepcopy(entityfactories.player)))


def main():
    screenWidth = 80
    screenHeight = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entityfactories.player)

    stateMachine = StateMachine(MainMenuState(player))

    with tcod.context.new_terminal(
        screenWidth,
        screenHeight,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        rootConsole = tcod.Console(screenWidth, screenHeight, order="F")
        while True:
            stateMachine.render(rootConsole, context)


if __name__ == '__main__':
    main()
