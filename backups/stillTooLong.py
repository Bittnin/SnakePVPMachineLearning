#bot

import math
from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]

def manhattanDistance(v1, v2):
    xd = v1.x - v2.x
    if xd < 0:
        xd = -xd
    yd = v1.y - v2.y
    if yd < 0:
        yd = -yd
    return xd + yd

distances = []
for b in bonuses:
    distances.append(manhattanDistance(mySnake.head(), b.position))

values = []
# Green
if distances[0] != 0:
    values.append((bonuses[0].score + bonuses[0].additive * distances[0]) / distances[0] * 1.5)
else:
    values.append(0)
# Red
if distances[1] != 0:
    values.append(bonuses[1].score * bonuses[1].multiplicative ** distances[1] / (distances[1] * 1.5))
else:
    values.append(0)
# Yellow
if distances[2] != 0:
    values.append((bonuses[2].score + bonuses[2].additive * distances[2] + len(mySnake.positions)) / (distances[2] * 1.5))
else:
    values.append(0)
# White/Blue/Diamant(scheiß drauf)
values.append(0)

b = bonuses[values.index(max(values))]

# find the shortest path to the current bonus and add the path to the list of tuples
p = []
bx = b.position.x
by = b.position.y  # y is 0 at the top of the map
cx = mySnake.head().x
cy = mySnake.head().y
reached = False
while not reached:
    nearest = 5000
    for d in range(0,4):
        dirc = Direction.RIGHT
        if d == 1:
            dirc = Direction.LEFT
        elif d == 2:
            dirc = Direction.UP
        elif d == 3:
            dirc = Direction.DOWN
        currentVector = world.move_and_teleport(Vector(cx, cy), dirc)
        if not world.obstacle(currentVector) and nearest > manhattanDistance(b.position, currentVector):
            nearest = manhattanDistance(b.position, currentVector)
            best = currentVector
            firstStep = dirc
    p.append(best)
    cx = best.x
    cy = best.y
    if b.position == best:
        reached = True
        break
mySnake.direction = firstStep