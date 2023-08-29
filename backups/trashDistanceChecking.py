# bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]

viableGoals = []
for b in bonuses:
    if b.effect == Effect.REVERSE:
        break
    # find the shortest path to the current bonus and add the path to the list of tuples
    p = []
    bx = b.position.x
    by = b.position.y  # y is 0 at the top of the map
    cx = mySnake.head().x
    cy = mySnake.head().y
    reached = False
    while reached == False:
        if cx > bx:  # my snake is to the right of the bonus
            if not world.obstacle(Vector(cx-1, cy)):
                cx -= 1
                p.append(Vector(cx, cy))
                continue

    viableGoals.append((b, p))

# check if the specific path would cause the snake to tangle up
path: List[Vector]
path = path[-len(mySnake.positions):]  # this will get the last {length} elements of the list
for g in viableGoals:
    # test if it is surrounded by obstacles & the own snake
    x = g.position.x
    y = g.position.y
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
            viableGoals.remove(g)
            break
