#bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs
import torch
import random
from collections import deque
import numpy as np
import yaml
from model import Linear_QNet, QTrainer

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]

# parameters
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # learning rate, aka how much the reward effects the nn


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness of choices
        self.gamma = 0.9  # discount rate, aka how much a higher reward later compensates a lower immediate one
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(17, 256, 3)  # TODO
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # TODO

    def get_state(self):  # simplify all the data into a game state
        state = []

        head = mySnake.head()

        # obstacles nearby
        for d in Direction:
            state.append(world.obstacle(head, d))

        state.append(mySnake.direction == Direction.UP)
        state.append(mySnake.direction == Direction.RIGHT)
        state.append(mySnake.direction == Direction.DOWN)
        state.append(mySnake.direction == Direction.LEFT)

        # TODO: change this to actually give more data about the food
        # for now its just targeting apples
        food = None
        for b in bonuses:
            if b.additive > 0.3:
                food = b.position

        # in which direction the food is
        state.append(food.x > head.x)
        state.append(food.x < head.x)
        state.append(food.y > head.y)
        state.append(food.y < head.y)

        enemy = other_snakes[0].head()

        # if we are closer
        state.append(head.dist(food) < enemy.dist(food))

        # in which direction the enemy is
        state.append(enemy.x > head.x)
        state.append(enemy.x < head.x)
        state.append(enemy.y > head.y)
        state.append(enemy.y < head.y)

        return np.array(state, dtype=int)

    def remember(self, old_state, action, reward, new_state):
        self.memory.append((old_state, action, reward, new_state))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        old_states, actions, rewards, new_states = zip(*mini_sample)
        self.trainer.train_step(old_states, actions, rewards, new_states)

    def train_short_memory(self, old_state, action, reward, new_state):
        self.trainer.train_step(old_state, action, reward, new_state)
        pass

    def get_action(self, state):
        # random moves to explore the environment
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dytpe=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


# read out the memory
with open('memory.yml', 'r') as f:
    memory = yaml.safe_load(f)

# statistics
plot_score = memory['plot_score']
plot_mean_score = memory['plot_mean_score']
total_score = memory['total_score']
record = memory['record']

agent = Agent()

agent.memory = memory['memory']
agent.n_games = memory['n_games']
agent.epsilon = memory['epsilon']

# get state
state = agent.get_state()

# get move
action = agent.get_action(state)

if action == 1:  # 0 is stay straight, 1 is turn left, 2 is turn right
    if mySnake.direction == Direction.UP:
        mySnake.direction = Direction.LEFT
    elif mySnake.direction == Direction.LEFT:
        mySnake.direction = Direction.DOWN
    elif mySnake.direction == Direction.DOWN:
        mySnake.direction = Direction.RIGHT
    else:
        mySnake.direction = Direction.UP
elif action == 2:
    if mySnake.direction == Direction.UP:
        mySnake.direction = Direction.RIGHT
    elif mySnake.direction == Direction.RIGHT:
        mySnake.direction = Direction.DOWN
    elif mySnake.direction == Direction.DOWN:
        mySnake.direction = Direction.LEFT
    else:
        mySnake.direction = Direction.UP

memory['last_action'] = action
memory['last_state'] = state
memory['last_score'] = mySnake.score
memory['last_move'] = mySnake.direction
memory['memory'] = agent.memory
memory['epsilon'] = agent.epsilon

if world.timer == 1:
    agent.train_long_memory()

    if mySnake.score > record:
        memory['record'] = mySnake.score
    memory['n_games'] += 1

with open('memory.yml', 'w') as f:
    yaml.dump(memory, f)

agent.model.save()
