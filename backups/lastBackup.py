#bot

import math
from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake
import world as hs

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]


def manhattan_distance(v1, v2):
    xd = v1.x - v2.x
    if xd < 0:
        xd = -xd
    yd = v1.y - v2.y
    if yd < 0:
        yd = -yd
    return xd + yd


distances = []
for r in range(0, 3):
    distances.append(manhattan_distance(mySnake.head(), bonuses[r].position))

b = bonuses[distances.index(min(distances))]

# find the shortest path to the current bonus and add the path to the list of tuples
bx = b.position.x
by = b.position.y
cx = mySnake.head().x
cy = mySnake.head().y
nearest = math.inf
firstStep = Direction.LEFT
for d in range(0, 4):
    dirc = Direction.RIGHT
    if d == 1:
        dirc = Direction.LEFT
    elif d == 2:
        dirc = Direction.UP
    elif d == 3:
        dirc = Direction.DOWN
    currentVector = world.move_and_teleport(Vector(cx, cy), dirc)
    for a in range(1, 2):
        checks = [Vector(cx, cy + a), Vector(cx, cy - a), Vector(cx + a, cy), Vector(cx - a, cy)]
        failed = 0
        for c in checks:
            try:
                if world.obstacle(c):
                    failed += 1
            except:
                pass
    if not world.obstacle(currentVector) and nearest > manhattan_distance(b.position, currentVector)\
            and failed <= 3:
        nearest = manhattan_distance(b.position, currentVector)
        best = currentVector
        firstStep = dirc

mySnake.direction = firstStep
