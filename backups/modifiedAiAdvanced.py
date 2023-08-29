#bot

from typing import List
import snake_types
from snake_types import Collectable, Vector, Direction, Snake, Effect
import world as hs

world: hs.World
mySnake: snake_types.Snake
bonuses: List[Collectable]
obstacles: List[Vector]
other_snakes: List[Snake]

dist = [[(world.width * world.height * 100, Direction.UP) for _ in range(world.width)] for _ in range(world.height)]
position = mySnake.head()
dist[position.x][position.y] = (0, Direction.UP)
current = []
up = world.move_and_teleport(position, Direction.UP)
down = world.move_and_teleport(position, Direction.DOWN)
left = world.move_and_teleport(position, Direction.LEFT)
right = world.move_and_teleport(position, Direction.RIGHT)

if not world.obstacle(up):
    dist[up.x][up.y] = (1, Direction.UP)
    current.append(up)

if not world.obstacle(down):
    dist[down.x][down.y] = (1, Direction.DOWN)
    current.append(down)

if not world.obstacle(left):
    dist[left.x][left.y] = (1, Direction.LEFT)
    current.append(left)

if not world.obstacle(right):
    dist[right.x][right.y] = (1, Direction.RIGHT)
    current.append(right)

while len(current) > 0:
    now = current.pop()
    cur_dist, cur_dir = dist[now.x][now.y]
    for d in Direction:
        next = world.move_and_teleport(now, d)
        if not world.obstacle(next):
            dst, direction = dist[next.x][next.y]
            if dst > cur_dist + 1:
                dist[next.x][next.y] = (cur_dist+1, cur_dir)
                current = [next] + current

maximaler_mehrwert = 0
beste_richtung = Direction.UP
target = None
bonusPositions = []
for bonus in bonuses:
    if bonus.effect == Effect.REVERSE:
        continue
    bonusPositions.append(bonus.position)
    d, direction = dist[bonus.position.x][bonus.position.y]
    wert = (bonus.get_current_score() * 1.1) / d
    if Vector.dist(mySnake.head(), bonus.position) * 1.1 > Vector.dist(other_snakes[0].head(), bonus.position):
        wert *= 0.3
    if bonus.effect == Effect.HALF and len(mySnake.positions) > 50:
        wert *= len(mySnake.positions) / 1.5
    # Schritt 3: Falls ein neues maximum gefunden ist, wollen wir dorthin gehen
    if wert > maximaler_mehrwert:
        beste_richtung = direction
        target = bonus.position
        maximaler_mehrwert = wert

# Bonus neben dran auch noch einsacken
for d in Direction:
    if world.move_and_teleport(mySnake.head(), d) in bonusPositions:
        beste_richtung = d

mySnake.direction = beste_richtung
