import random
from typing import Iterator, List, Tuple
import tcod

from gamemap import GameMap
from intersection import intersect
from room import RectangularRoom
from entity import Entity
import entityfactories
import tiletypes


def tunnelBetween(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        cornerX, cornerY = x2, y1
    else:
        cornerX, cornerY = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y


def generateDungeon(
    maxRooms: int,
    roomMinSize: int,
    roomMaxSize: int,
    mapWidth: int,
    mapHeight: int,
    maxMonstersPerRoom: int,
    maxItemsPerRoom: int,
    player: Entity,
) -> GameMap:
    dungeon = GameMap(mapWidth, mapHeight, entities=[player], player=player)

    rooms: List[RectangularRoom] = []

    for r in range(maxRooms):
        roomWidth = random.randint(roomMinSize, roomMaxSize)
        roomHeight = random.randint(roomMinSize, roomMaxSize)

        x = random.randint(0, dungeon.width - roomWidth - 1)
        y = random.randint(0, dungeon.height - roomHeight - 1)

        newRoom = RectangularRoom(x, y, roomWidth, roomHeight)

        if any(intersect(newRoom, otherRoom) for otherRoom in rooms):
            continue

        dungeon.tiles[newRoom.inner] = tiletypes.floor

        if len(rooms) == 0:
            player.x, player.y = newRoom.center
        else:
            for x, y in tunnelBetween(rooms[-1].center, newRoom.center):
                dungeon.tiles[x, y] = tiletypes.floor

        placeEntities(newRoom, dungeon, maxMonstersPerRoom, maxItemsPerRoom)

        rooms.append(newRoom)

    return dungeon


def placeEntities(room: RectangularRoom, dungeon: GameMap, maxMonstersPerRoom: int, maxItemsPerRoom: int) -> None:
    nbMonsters = random.randint(0, maxMonstersPerRoom)

    for i in range(nbMonsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entityfactories.spawnEntity(entityfactories.orc, dungeon, x, y)
            else:
                entityfactories.spawnEntity(entityfactories.troll, dungeon, x, y)

    nbItems = random.randint(0, maxItemsPerRoom)

    for i in range(nbItems):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            r = random.random()
            if r < 0.3:
                entityfactories.spawnEntity(entityfactories.lightningScroll, dungeon, x, y)
            elif r < 0.4:
                entityfactories.spawnEntity(entityfactories.confusionScroll, dungeon, x, y)
            elif r < 0.5:
                entityfactories.spawnEntity(entityfactories.fireballScroll, dungeon, x, y)
            else:
                entityfactories.spawnEntity(entityfactories.healthPotion, dungeon, x, y)
