#bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.optimizers import adam_v2
import numpy as np
import random

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]
