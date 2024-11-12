import pygame
from snake import Snake, check_collision
from food import Food
from a_star import a_star_search
from vars import WIDTH, HEIGHT, BLACK, WHITE

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with A*")
clock = pygame.time.Clock()

def draw_text(window, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def game_loop():
    snake = Snake()
    food = Food(snake)
    path = []
    score = 0
    speed = 5
    font = pygame.font.Font(None, 30)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not path:
            path = a_star_search(snake, food)
        
        if path:
            next_move = path.pop(0)
            snake.direction = (next_move[0] - snake.body[0][0], next_move[1] - snake.body[0][1])
            snake.move()

        if check_collision(snake, food):
            snake.grow()
            food = Food(snake)
            path = []
            speed += 1
            score += 1

        window.fill(BLACK)

        snake.draw(window)
        food.draw(window)

        
        draw_text(window, f"Comida: {score}", font, WHITE, 10, 10)
        draw_text(window, f"Velocidad: {speed}", font, WHITE, 10, 40)

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

game_loop()