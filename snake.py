import pygame
from vars import GREEN, GRID_SIZE, HEIGHT, WIDTH

class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = (0, -1)
        self.growth_pending = 0 

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if not (0 <= new_head[0] < WIDTH // GRID_SIZE and 0 <= new_head[1] < HEIGHT // GRID_SIZE):
            return False 

        if new_head in self.body:
            return False

        if self.growth_pending > 0:
            self.body = [new_head] + self.body  # Crece
            self.growth_pending -= 1
        else:
            self.body = [new_head] + self.body[:-1]

        return True

    def grow(self):
        self.growth_pending += 1

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, GREEN, pygame.Rect(segment[0] * GRID_SIZE -2, segment[1] * GRID_SIZE -2, GRID_SIZE -2, GRID_SIZE -2))

def check_collision(snake, food):
    if snake.body[0] == food.position:
        return True
    return False
