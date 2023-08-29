#bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs
import numpy as np
import random
import pickle

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.rand(input_size, hidden_size)
        self.weights2 = np.random.rand(hidden_size, output_size)

    def forward(self, X):
        self.z1 = np.dot(X, self.weights1)
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.weights2)
        y_hat = self.sigmoid(self.z2)
        return y_hat

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def save_model(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.nn, file)

    def load_model(self, file_name):
        with open(file_name, 'rb') as file:
            self.nn = pickle.load(file)


class Agent:
    def __init__(self, input_size, hidden_size, output_size):
        self.nn = NeuralNetwork(input_size, hidden_size, output_size)
        self.memory = []

    def get_action(self, state):
        action_values = self.nn.forward(state)
        action_index = np.argmax(action_values)
        return Direction(action_index)

    def update_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.nn.forward(next_state)
            target_f = self.nn.forward(state)
            target_f[action] = target
            self.nn.train(state, target_f)


agent = Agent(4, 4,4)

# Load the model and the latest state and action
try:
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    agent.nn = data['model']
    old_state = data['state']
    action = data['action']
except FileNotFoundError:
    old_state = (0, 0, 0, 0, 0)
    action = agent.get_action(old_state)

# Get the current state
scores = []
for p in world.players:
    scores.append(p.score)
state = (mySnake.positions, obstacles, bonuses, other_snakes[0].positions, scores)

# Calculate the reward
previousScore = 0
with open("score.txt", 'r') as f:
    previousScore = int(str(f.readline(1)))
with open("score.txt", 'w') as f:
    f.flush()
    f.write(str(scores[0]))

reward = -1.0
if scores[0] > previousScore:
    reward = 1.0
elif scores[0] == previousScore:
    reward = 0.0

# Update the agent's memory and train the agent
agent.update_memory(old_state, action.value, reward, state, False)
agent.train(1)

# Get the next action
action = agent.get_action(state)

# Save the model and the latest state and action
with open('model.pkl', 'wb') as file:
    data = {
        'model': agent.nn,
        'state': state,
        'action': action
    }
    pickle.dump(data, file)

# Output the next direction
mySnake.direction = action
