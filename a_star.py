from vars import WIDTH, GRID_SIZE, HEIGHT

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position):
    x, y = position
    neighbors = [
        (x - 1, y),  # Izquierda
        (x + 1, y),  # Derecha
        (x, y - 1),  # Arriba
        (x, y + 1)   # Abajo
    ]

    valid_neighbors = [
        (nx, ny) for (nx, ny) in neighbors
        if 0 <= nx < WIDTH // GRID_SIZE and 0 <= ny < HEIGHT // GRID_SIZE
    ]
    return valid_neighbors

def a_star_search(snake, food):
    start = snake.body[0]
    goal = food.position
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = frontier.pop(0)[1]

        if current == goal:
            break

        neighbors = get_neighbors(current)

        for next_position in neighbors:
            if next_position in snake.body:
                continue

            new_cost = cost_so_far[current] + 1
            if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                cost_so_far[next_position] = new_cost
                priority = new_cost + heuristic(goal, next_position)
                frontier.append((priority, next_position))
                came_from[next_position] = current

    current = goal
    path = []
    while current != start:
        if current not in came_from:
            print("No se encontró un camino válido.")
            return []
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
