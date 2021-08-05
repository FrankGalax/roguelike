from room import RectangularRoom


def intersect(room: RectangularRoom, otherRoom: RectangularRoom):
    return (room.x1 <= otherRoom.x2
            and room.x2 >= otherRoom.x1
            and room.y1 <= otherRoom.y2
            and room.y2 >= otherRoom.y1
            )
