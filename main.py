#!/usr/bin/env python3
import tcod
import copy

from engine import Engine
from inputhandlers import EventHandler
import entityfactories


def main():
    screenWidth = 80
    screenHeight = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entityfactories.player)

    eventHandler = EventHandler(player)

    engine = Engine(player=player)

    with tcod.context.new_terminal(
        screenWidth,
        screenHeight,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        rootConsole = tcod.Console(screenWidth, screenHeight, order="F")
        while True:
            engine.render(console=rootConsole, context=context)

            events = tcod.event.wait()

            engine.handleEvents(events, context)


if __name__ == '__main__':
    main()
