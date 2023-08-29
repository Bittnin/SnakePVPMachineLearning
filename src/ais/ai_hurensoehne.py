#bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs
import tensorflow

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]
