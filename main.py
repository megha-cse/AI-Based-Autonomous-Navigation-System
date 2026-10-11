
import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Window settings
CELL_SIZE = 40
COLS = 15
ROWS = 12
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI-Based Autonomous Navigation System")

# Colours
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (210, 210, 210)
GREEN = (50, 200, 100)
RED = (240, 70, 70)
BLUE = (60, 120, 255)
YELLOW = (255, 210, 60)

font = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()

# Start, goal and obstacles
start = (0, 0)
goal = (14, 11)

obstacles = {
    (3, 0), (3, 1), (3, 2), (3, 3),
    (3, 4), (3, 5), (5, 6), (6, 6),
    (7, 6), (8, 6), (9, 6), (10, 6),
    (10, 7), (10, 8), (10, 9),
    (6, 2), (7, 2), (8, 2),
    (12, 3), (12, 4), (12, 5)
}

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path():
    frontier = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nxt = (current[0] + dx, current[1] + dy)

            if not (0 <= nxt[0] < COLS and 0 <= nxt[1] < ROWS):
                continue
            if nxt in obstacles:
                continue

            new_cost = cost[current] + 1

            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    if goal not in came_from:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    return path[::-1]

path = find_path()
robot_index = 0
last_move = 0
move_delay = 180

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                robot_index = 0
                path = find_path()
                last_move = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    if path and robot_index < len(path) - 1:
        if now - last_move >= move_delay:
            robot_index += 1
            last_move = now

    screen.fill(WHITE)

    # Draw grid
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(
                x * CELL_SIZE, y * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw obstacles
    for x, y in obstacles:
        pygame.draw.rect(
            screen, BLACK,
            (x * CELL_SIZE + 2, y * CELL_SIZE + 2,
             CELL_SIZE - 4, CELL_SIZE - 4)
        )

    # Draw planned path
    for x, y in path:
        pygame.draw.circle(
            screen, YELLOW,
            (x * CELL_SIZE + CELL_SIZE // 2,
             y * CELL_SIZE + CELL_SIZE // 2),
            6
        )

    # Draw start and goal
    pygame.draw.rect(
        screen, GREEN,
        (start[0] * CELL_SIZE + 4, start[1] * CELL_SIZE + 4,
         CELL_SIZE - 8, CELL_SIZE - 8)
    )

    pygame.draw.rect(
        screen, RED,
        (goal[0] * CELL_SIZE + 4, goal[1] * CELL_SIZE + 4,
         CELL_SIZE - 8, CELL_SIZE - 8)
    )

    # Draw robot
    if path:
        rx, ry = path[robot_index]
        pygame.draw.circle(
            screen, BLUE,
            (rx * CELL_SIZE + CELL_SIZE // 2,
             ry * CELL_SIZE + CELL_SIZE // 2),
            13
        )

    # Display information
    info = font.render(
        "A* Navigation | R: Restart | ESC: Exit",
        True, BLACK
    )
    screen.blit(info, (8, ROWS * CELL_SIZE + 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
