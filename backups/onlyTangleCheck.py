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

viableGoals = bonuses.copy()

# check if the specific path would cause the snake to tangle up
path: List[Vector]
path = path[-len(mySnake.positions):] # this will get the last n elements of the path where n is the curren snake length
for g in viableGoals:
    # test if it is surrounded by obstacles & the own snake
    x = g.position.x
    y = g.position.y
    for d in range(1, 4): # repeat for multiple check distances from the starting point
        checks = [Vector(x, y+d), Vector(x, y-d), Vector(x+d, y), Vector(x-d, y)]
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
