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

viableGoals = []
for b in bonuses:
    if b.effect == Effect.REVERSE:
        continue
    # find the shortest path to the current bonus and add the path to the list of tuples
    p = []
    bx = b.position.x
    by = b.position.y  # y is 0 at the top of the map
    cx = mySnake.head().x
    cy = mySnake.head().y
    reached = False
    while not reached:
        nearest = math.inf
        best = Vector()
        firstStep = Direction.LEFT
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
    viableGoals.append((b, p, firstStep))

# check if the specific path would cause the snake to tangle up
for t in viableGoals:
    # test if it is surrounded by obstacles & the own snake
    x = t[0].position.x
    y = t[0].position.y

    path = t[1][-len(mySnake.positions):]  # this will get the last {length} elements of the list
    for d in range(1, 4):  # repeat for multiple check distances from the starting point
        checks = [Vector(x, y + d), Vector(x, y - d), Vector(x + d, y), Vector(x - d, y)]
        failed = 0
        for c in checks:
            if c in path:
                failed += 1
            elif c in obstacles:
                failed += 1
            elif c in other_snakes[0].positions:
                failed += 1
        if failed > 3:
            viableGoals.remove(t)
            break

mySnake.direction = viableGoals[0][2]