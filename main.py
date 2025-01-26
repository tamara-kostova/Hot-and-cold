import random
import pygame
import os

pygame.init()

TILE_SIZE = 70
GRID_WIDTH = 16
GRID_HEIGHT = 10

SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duck Board Game")


ASSETS_DIR = "assets"


LAVA_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "lava.png")).convert_alpha()
WATER_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "water.png")).convert_alpha()
WALL_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "wall.png")).convert_alpha()
EMPTY_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "empty.png")).convert_alpha()
DUCK_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "duck.png")).convert_alpha()
ICE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "ice.png")).convert_alpha()
BOX_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "box.png")).convert_alpha()
PORTAL_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "portal.png")).convert_alpha()
COLLECTIBLE_IMG = pygame.image.load(
    os.path.join(ASSETS_DIR, "collectible.png")
).convert_alpha()
IMMUNITY_IMG = pygame.image.load(
    os.path.join(ASSETS_DIR, "immunity.png")
).convert_alpha()
TIMER_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "timer.png")).convert_alpha()


LAVA_IMG = pygame.transform.scale(LAVA_IMG, (TILE_SIZE, TILE_SIZE))
WATER_IMG = pygame.transform.scale(WATER_IMG, (TILE_SIZE, TILE_SIZE))
WALL_IMG = pygame.transform.scale(WALL_IMG, (TILE_SIZE, TILE_SIZE))
EMPTY_IMG = pygame.transform.scale(EMPTY_IMG, (TILE_SIZE, TILE_SIZE))
DUCK_IMG = pygame.transform.scale(DUCK_IMG, (TILE_SIZE, TILE_SIZE))
ICE_IMG = pygame.transform.scale(ICE_IMG, (TILE_SIZE, TILE_SIZE))
BOX_IMG = pygame.transform.scale(BOX_IMG, (TILE_SIZE, TILE_SIZE))
PORTAL_IMG = pygame.transform.scale(PORTAL_IMG, (TILE_SIZE, TILE_SIZE))
COLLECTIBLE_IMG = pygame.transform.scale(COLLECTIBLE_IMG, (TILE_SIZE, TILE_SIZE))
IMMUNITY_IMG = pygame.transform.scale(IMMUNITY_IMG, (TILE_SIZE, TILE_SIZE))
TIMER_IMG = pygame.transform.scale(TIMER_IMG, (TILE_SIZE, TILE_SIZE))


clock = pygame.time.Clock()
FPS = 60

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

LEVELS = [
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 7, 0, 0, 4, 4, 4, 0, 3],
        [3, 0, 5, 0, 0, 0, 6, 4, 4, 3],
        [3, 0, 0, 0, 7, 0, 0, 0, 2, 3],
        [3, 0, 0, 0, 0, 0, 0, 7, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 7, 0, 0, 4, 4, 4, 0, 4, 0, 3],
        [3, 0, 5, 0, 0, 0, 6, 4, 4, 4, 4, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 2, 7, 2, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 0, 0, 0, 0, 0, 0, 1, 0, 7, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 5, 0, 0, 0, 6, 0, 0, 10, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 7, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 3],
        [3, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
]

EMPTY = 0
LAVA = 1
WATER = 2
WALL = 3
ICE = 4
BOX = 5
PORTAL = 6
COLLECTIBLE = 7
IMMUNITY = 8
TIMER = 10

timers = {}
immunity_moves = 0


def draw_grid(grid):
    for y, row in enumerate(grid):
        for x in range(len(row)):
            screen.blit(EMPTY_IMG, (x * TILE_SIZE, y * TILE_SIZE))
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == EMPTY:
                screen.blit(EMPTY_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == LAVA:
                screen.blit(LAVA_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == WATER:
                screen.blit(WATER_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == WALL:
                screen.blit(WALL_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == ICE:
                screen.blit(ICE_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == BOX:
                screen.blit(BOX_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == PORTAL:
                screen.blit(PORTAL_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == COLLECTIBLE:
                screen.blit(COLLECTIBLE_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == IMMUNITY:
                screen.blit(IMMUNITY_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == TIMER:
                screen.blit(TIMER_IMG, (x * TILE_SIZE, y * TILE_SIZE))
                if (x, y) in timers:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(timers[(x, y)]), True, BLACK)
                    screen.blit(text, (x * TILE_SIZE + 25, y * TILE_SIZE + 25))


def spread_tiles(grid):
    global immunity_moves
    height = len(grid)
    width = len(grid[0])
    new_grid = [row[:] for row in grid]

    if immunity_moves > 0:
        immunity_moves -= 1
        return grid

    for y in range(height):
        for x in range(width):
            if grid[y][x] == LAVA:
                for dx, dy in DIRECTIONS.values():
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[ny][nx] == WATER:
                            new_grid[ny][nx] = WALL
                        elif grid[ny][nx] == EMPTY:
                            new_grid[ny][nx] = LAVA
            elif grid[y][x] == WATER:
                for dx, dy in DIRECTIONS.values():
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[ny][nx] == EMPTY:
                            new_grid[ny][nx] = WATER
    return new_grid


def update_timers(grid):
    global timers
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == TIMER:
                if (x, y) not in timers:
                    timers[(x, y)] = 15
                else:
                    if grid[y][x] == BOX:
                        continue
                    timers[(x, y)] -= 1
                    if timers[(x, y)] <= 0:
                        grid[y][x] = LAVA
                        del timers[(x, y)]


def is_duck_valid(grid, duck_pos):
    x, y = duck_pos
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        tile = grid[y][x]
        return tile not in [LAVA, WALL]
    return False


def welcome_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    instructions = [
        "Welcome to Duck Board Game!",
        "Instructions:",
        "1. Use arrow keys to move the duck.",
        "2. Collect all collectibles to unlock the portal.",
        "3. Avoid lava or you'll lose!",
        "4. Push boxes to block lava or cover timed tiles.",
        "5. Water spreads but is safe to swim on.",
        "6. Use power-ups to survive!",
        "Press any key to start.",
    ]

    y_offset = 100
    for line in instructions:
        text = font.render(line, True, BLACK)
        screen.blit(text, (50, y_offset))
        y_offset += 40

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def display_message(message, color):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    global timers, immunity_moves
    welcome_screen()
    level_index = 0
    grid = [row[:] for row in LEVELS[level_index]]
    duck_pos = [1, 1]
    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

                new_pos = [duck_pos[0] + dx, duck_pos[1] + dy]
                if 0 <= new_pos[0] < len(grid[0]) and 0 <= new_pos[1] < len(grid):
                    target_tile = grid[new_pos[1]][new_pos[0]]
                    if target_tile == LAVA and immunity_moves == 0:
                        display_message("Game Over!", RED)
                        running = False
                    elif target_tile in [EMPTY, WATER, IMMUNITY]:
                        duck_pos = new_pos
                        if target_tile == IMMUNITY:
                            immunity_moves = random.randint(3, 7)
                            grid[new_pos[1]][new_pos[0]] = EMPTY
                    elif target_tile in [EMPTY, WATER, IMMUNITY] or (
                        target_tile == LAVA and immunity_moves > 0
                    ):
                        duck_pos = new_pos
                    elif target_tile == ICE:
                        while True:
                            new_pos[0] += dx
                            new_pos[1] += dy
                            if not (
                                0 <= new_pos[0] < len(grid[0])
                                and 0 <= new_pos[1] < len(grid)
                            ):
                                break
                            if grid[new_pos[1]][new_pos[0]] != ICE:
                                if grid[new_pos[1]][new_pos[0]] == LAVA:
                                    display_message("Game Over!", RED)
                                    running = False
                                duck_pos = new_pos
                                break
                    elif target_tile == COLLECTIBLE:
                        duck_pos = new_pos
                        grid[new_pos[1]][new_pos[0]] = EMPTY
                    elif target_tile == BOX:
                        box_new_pos = [new_pos[0] + dx, new_pos[1] + dy]
                        if (
                            0 <= box_new_pos[0] < len(grid[0])
                            and 0 <= box_new_pos[1] < len(grid)
                            and grid[box_new_pos[1]][box_new_pos[0]]
                            in [EMPTY, WATER, LAVA, TIMER]
                        ):
                            grid[box_new_pos[1]][box_new_pos[0]] = BOX
                            grid[new_pos[1]][new_pos[0]] = EMPTY
                            duck_pos = new_pos
                    elif target_tile == PORTAL:
                        if not any(COLLECTIBLE in row for row in grid):
                            level_index += 1
                            if level_index < len(LEVELS):
                                grid = [row[:] for row in LEVELS[level_index]]
                                duck_pos = [1, 1]
                                timers = {}
                            else:
                                display_message("You Win!", GREEN)
                                running = False

                grid = spread_tiles(grid)
                update_timers(grid)
                if not is_duck_valid(grid, duck_pos):
                    display_message("Game Over!", RED)
                    running = False

        draw_grid(grid)
        screen.blit(DUCK_IMG, (duck_pos[0] * TILE_SIZE, duck_pos[1] * TILE_SIZE))

        if immunity_moves > 0:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Immunity: {immunity_moves} moves", True, GREEN)
            screen.blit(text, (SCREEN_WIDTH - 200, 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
