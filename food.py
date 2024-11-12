import random
import pygame
from vars import WIDTH, GRID_SIZE, RED, HEIGHT

class Food:
    def __init__(self, snake):
        self.position = self.generate_food(snake)

    def generate_food(self, snake):
        while True:
            position = (random.randint(0, WIDTH // GRID_SIZE - 1), random.randint(0, HEIGHT // GRID_SIZE - 1))
            if position not in snake.body:
                return position

    def draw(self, window):
        pygame.draw.rect(window, RED, pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
