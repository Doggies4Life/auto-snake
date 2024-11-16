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

def movement_cost(current, next_position, previous=None):
    cost = 14
    if previous:
        if (current[0] == previous[0] and next_position[0] == current[0]) or \
           (current[1] == previous[1] and next_position[1] == current[1]):
            cost = 10
    return cost

def a_star_search(snake, food):
    start = snake.body[0]
    goal = food.position
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    previous = None

    while frontier:
        frontier.sort(key=lambda x: x[0])
        current = frontier.pop(0)[1]

        if current == goal:
            break

        neighbors = get_neighbors(current)

        for next_position in neighbors:
            if next_position in snake.body:
                continue

            if previous is not None and len(snake.body) > 1 and next_position == snake.body[1]:
                continue

            movement_cost_value = movement_cost(current, next_position, previous)
            new_cost = cost_so_far[current] + movement_cost_value

            if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                cost_so_far[next_position] = new_cost
                priority = new_cost + heuristic(goal, next_position)
                frontier.append((priority, next_position))
                came_from[next_position] = current

        previous = current

    current = goal
    path = []
    while current != start:
        if current not in came_from:
            print("No se encontró un camino")
            return path
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


def evaluate_future_space(snake, path):
    simulated_snake = list(snake.body)
    
    for step in path:
        simulated_snake.insert(0, step)
        simulated_snake.pop()

    free_space = 0
    grid_width = WIDTH // GRID_SIZE
    grid_height = HEIGHT // GRID_SIZE

    for x in range(grid_width):
        for y in range(grid_height):
            if (x, y) not in simulated_snake:
                free_space += 1

    min_safe_space = len(simulated_snake) + 5

    return free_space >= min_safe_space

def generate_safe_cycle(snake, path):
    head = snake.body[0]
    cycle = []
    neighbors = get_neighbors(head)
    for neighbor in neighbors:
        if neighbor not in snake.body and neighbor not in path:
            cycle.append(neighbor)
    cycle.sort(key=lambda pos: heuristic(head, pos))
    return cycle

def simulate_snake_growth_extended(snake, path, depth=150):
    simulated_snake = list(snake.body)

    for step in path:
        simulated_snake.insert(0, step)
        simulated_snake.pop()
    
    head = simulated_snake[0]

    for _ in range(depth):
        neighbors = get_neighbors(head)
        future_move = False
        for neighbor in neighbors:
            if neighbor not in simulated_snake:
                simulated_snake.insert(0, neighbor)
                simulated_snake.pop()
                head = neighbor
                future_move = True
                break
        
        if not future_move:
            return False

    return True

def a_star_search_with_safe_cycle(snake, food):
    path = a_star_search(snake, food)

    if path:
        if simulate_snake_growth_extended(snake, path) and evaluate_future_space(snake, path):
            return path  
        else:
            return generate_safe_cycle(snake, path)
    
    safe_cycle = generate_safe_cycle(snake, path)
    
    if safe_cycle and evaluate_future_space(snake, safe_cycle):
        return path 
    else:
        return []