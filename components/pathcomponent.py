from typing import List, Tuple
import numpy as np
import tcod

from components.component import Component
from gamemap import GameMap


class PathComponent(Component):
    def __init__(self):
        super().__init__()
        self.path: List[Tuple[int, int]] = []

    def onOwnerChanged(self):
        self.owner.pathComponent = self

    def setPathTo(self, gamemap: GameMap, destX: int, destY: int):
        cost = np.array(gamemap.tiles["walkable"], dtype=np.int8)

        for entity in gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocksMovement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.owner.x, self.owner.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((destX, destY))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        self.path = [(index[0], index[1]) for index in path]

    def clearPath(self):
        self.path.clear()
