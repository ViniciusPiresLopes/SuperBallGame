import pygame
import random
import time

pygame.init()

# Colors
WHITE = 255, 255, 255,
BLACK = 0, 0, 0,
GREEN = 0, 255, 0,
RED = 255, 0, 0,

# Window setup
FPS = 60

clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720
background_color = WHITE
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Ball Game!")

# Functions
def is_ball_overlapping(ball1, ball2):
    dx = ball1.pos[0] - ball2.pos[0]
    dy = ball1.pos[1] - ball2.pos[1]
    r = ball1.radius + ball2.radius

    return (dx ** 2 + dy ** 2) < (r ** 2)


def is_point_in_ball(ball, px, py):
    dx = ball.pos[0] - px
    dy = ball.pos[1] - py
    r = ball.radius

    return (dx ** 2 + dy ** 2) < (r ** 2)


def is_ball_inside_another(ball1, ball2):
    points = [
        (ball1.pos[0] - ball1.radius, ball1.pos[1]),
        (ball1.pos[0], ball1.pos[1] - ball1.radius),
        (ball1.pos[0] + ball1.radius, ball1.pos[1]),
        (ball1.pos[0], ball1.pos[1] + ball1.radius)
    ]

    for point in points:
        if is_point_in_ball(ball2, point[0], point[1]):
            continue
        return False

    return True


# Classes
class Ball:
    def __init__(self, color, radius, pos):
        self.color = color
        self.radius = radius
        self.pos = pos

    def draw(self, window):
        pygame.draw.circle(window, self.color, (round(self.pos[0]), round(self.pos[1])), round(self.radius))


class Player(Ball):
    def __init__(self, color, radius, pos, initial_speed):
        super().__init__(color, radius, pos)
        self.initial_speed = initial_speed
        self.boost = 1

    def set_boost(self, value):
        self.boost = value

    def move(self, direction):
        self.speed = self.initial_speed / self.radius * self.boost
        
        self.pos[0] += direction[0] * self.speed
        self.pos[1] += direction[1] * self.speed


# Main loop
players = []
players.append(Player((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 25, [random.randint(0, WIDTH), random.randint(0, HEIGHT)], 80))
players.append(Player((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 25, [random.randint(0, WIDTH), random.randint(0, HEIGHT)], 80))

fruits = []

start_time = 0
end_time = 0

running = True
while running:
    clock.tick(FPS)

    if (end_time - start_time) < 3:
        end_time = time.time()
    else:
        start_time = time.time()
        fruits.append(Ball(RED, random.randint(5, 20), [random.randint(0, WIDTH) - 15, random.randint(0, HEIGHT) - 15]))

    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()

    try:
        # Player 1 movements and wall collision
        if key[pygame.K_w] and players[0].pos[1] > players[0].radius:
            players[0].move((0, -1))

        if key[pygame.K_s] and players[0].pos[1] < HEIGHT - players[0].radius:
            players[0].move((0, 1))

        if key[pygame.K_a] and players[0].pos[0] > players[0].radius:
            players[0].move((-1, 0))

        if key[pygame.K_d] and players[0].pos[0] < WIDTH - players[0].radius:
            players[0].move((1, 0))
    except IndexError:
        pass

    try:
        # Player 2 movements and wall collision
        if key[pygame.K_UP] and players[1].pos[1] > players[1].radius:
            players[1].move((0, -1))

        if key[pygame.K_DOWN] and players[1].pos[1] < HEIGHT - players[1].radius:
            players[1].move((0, 1))

        if key[pygame.K_LEFT] and players[1].pos[0] > players[1].radius:
            players[1].move((-1, 0))

        if key[pygame.K_RIGHT] and players[1].pos[0] < WIDTH - players[1].radius:
            players[1].move((1, 0))
    except IndexError:
        pass
    
    # Players collision
    players_size = len(players)
    for i in range(players_size):
        for j in range(players_size):
            if i != j:
                try:
                    if is_ball_inside_another(players[i], players[j]):
                        players[j].radius += players[i].radius
                        players.pop(i)
                except IndexError:
                    pass

    # Fruit collision
    fruits_size = len(fruits)
    for i in range(fruits_size):
        for j in range(players_size):
            try:
                if is_ball_inside_another(fruits[i], players[j]):
                    players[0].set_boost(1)
                    players[1].set_boost(1)

                    if j == 1:
                        players[0].set_boost(1.25)
                    else:
                        players[1].set_boost(1.25)
                    
                    players[j].radius += fruits[i].radius
                    fruits.pop(i)
            except IndexError:
                pass

    # Draw
    window.fill(background_color)

    for fruit in fruits:
        fruit.draw(window)

    try:
        if players[0].radius > players[1].radius:
            players[1].draw(window)
            players[0].draw(window)
        else:
            players[0].draw(window)
            players[1].draw(window)
    except IndexError:
        for player in players:
            player.draw(window)
    
    pygame.display.flip()

pygame.quit()
