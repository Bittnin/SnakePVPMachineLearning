#bot

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
for b in bonuses:
    distances.append(manhattan_distance(mySnake.head(), b.position))
enemyDistances = []
for b in bonuses:
    enemyDistances.append(manhattan_distance(other_snakes[0].head(), b.position))

values = []
# Green
if distances[0] != 0 and enemyDistances[0] * 1.2 > distances[0]:
    values.append((bonuses[0].score) / (distances[0] * 1.5))
else:
    values.append(0)
# Red
if distances[1] != 0 and enemyDistances[1] * 1.2 > distances[1]:
    values.append((bonuses[1].score) / (distances[1] * 1.5))
else:
    values.append(0)
# Yellow
if distances[2] != 0 and enemyDistances[2] * 1.2 > distances[2] and len(mySnake.positions) <= 27:
    values.append((bonuses[2].score) / (distances[2] * 1.5))
elif distances[2] != 0 and enemyDistances[2] * 1.2 > distances[2]:
    values.append((bonuses[2].score + (len(mySnake.positions) * 5)) / (distances[2] * 1.5))
else:
    values.append(0)
# White/Blue/Diamant(scheiß drauf)
values.append(0)

b = bonuses[values.index(max(values))]

# find the shortest path to the current bonus and add the path to the list of tuples
bx = b.position.x
by = b.position.y
cx = mySnake.head().x
cy = mySnake.head().y
nearest = 5000
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
    if not world.obstacle(currentVector) and nearest > manhattan_distance(b.position, currentVector):
        nearest = manhattan_distance(b.position, currentVector)
        best = currentVector
        firstStep = dirc

for d in range(0, 4):
    x = world.move_and_teleport(mySnake.head(), firstStep).x
    y = world.move_and_teleport(mySnake.head(), firstStep).y
    for a in range(1, 4):  # repeat for multiple check distances from the starting point
        checks = [Vector(x, y + a), Vector(x, y - a), Vector(x + a, y), Vector(x - a, y)]
        failed = 0
        try:
            for c in checks:
                if world.obstacle(c):
                    failed += 1
        except:
            pass
        if failed > 3:
            break
    if firstStep == Direction.UP:
        firstStep = Direction.RIGHT
    elif firstStep == Direction.RIGHT:
        firstStep = Direction.DOWN
    elif firstStep == Direction.DOWN:
        firstStep = Direction.LEFT
    elif firstStep == Direction.LEFT:
        firstStep = Direction.UP

mySnake.direction = firstStep
