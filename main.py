import random
import pygame
import os

pygame.init()

TILE_SIZE = 70
GRID_WIDTH = 16
GRID_HEIGHT = 10

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HOT and COLD")

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
TELEPORT_IMG = pygame.image.load(
    os.path.join(ASSETS_DIR, "teleport.png")
).convert_alpha()
HEART_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "heart.png")).convert_alpha()

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
TELEPORT_IMG = pygame.transform.scale(TELEPORT_IMG, (TILE_SIZE, TILE_SIZE))
HEART_IMG = pygame.transform.scale(HEART_IMG, (TILE_SIZE*1.5, TILE_SIZE))

clock = pygame.time.Clock()
FPS = 60

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


def load_levels(filename):
    with open(filename, "r") as file:
        content = file.read().strip()
    levels = []
    for level_data in content.split("\n\n"):
        level = []
        for row in level_data.split("\n"):
            level.append([int(x) for x in row.split(",")])
        levels.append(level)
    return levels

LEVELS = load_levels("levels.txt")


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
TELEPORT = 11

timers = {}
immunity_moves = 0


undo_stack = []


teleporters = {
    (2, 2): (14, 2),
    (14, 2): (2, 2),
    (14, 7): (2, 2),
}


def draw_grid(grid):
    grid_width = len(grid[0]) * TILE_SIZE
    grid_height = len(grid) * TILE_SIZE

    offset_x = (SCREEN_WIDTH - grid_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_height) // 2

    for y, row in enumerate(grid):
        for x in range(len(row)):
            screen.blit(EMPTY_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y))
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == EMPTY:
                screen.blit(
                    EMPTY_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == LAVA:
                screen.blit(
                    LAVA_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == WATER:
                screen.blit(
                    WATER_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == WALL:
                screen.blit(
                    WALL_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == ICE:
                screen.blit(
                    ICE_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == BOX:
                screen.blit(
                    BOX_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == PORTAL:
                screen.blit(
                    PORTAL_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == COLLECTIBLE:
                screen.blit(
                    COLLECTIBLE_IMG,
                    (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y),
                )
            elif tile == IMMUNITY:
                screen.blit(
                    IMMUNITY_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
            elif tile == TIMER:
                screen.blit(
                    TIMER_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )
                if (x, y) in timers:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(timers[(x, y)]), True, BLACK)
                    screen.blit(
                        text,
                        (x * TILE_SIZE + offset_x + 25, y * TILE_SIZE + offset_y + 25),
                    )
            elif tile == TELEPORT:
                screen.blit(
                    TELEPORT_IMG, (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                )


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
        "Welcome to HOT and COLD!",
        "Instructions:",
        "1. Use arrow keys to move the duck.",
        "2. Collect all collectibles to unlock the portal.",
        "3. Avoid lava or you'll lose!",
        "4. Push boxes to block lava or cover timed tiles.",
        "5. Water spreads but is safe to swim on.",
        "6. Use power-ups to survive!",
        "7. Press 'U' to undo your last move.",
        "Press any key to start.",
    ]

    total_height = len(instructions) * 40
    start_y = (SCREEN_HEIGHT - total_height) // 2

    for i, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 40))
        screen.blit(text, text_rect)

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


def reset_level(level_index):
    global timers, immunity_moves, undo_stack
    grid = [row[:] for row in LEVELS[level_index]]
    duck_pos = [1, 1]
    timers = {}
    immunity_moves = 0
    undo_stack = []
    return grid, duck_pos


def save_state(grid, duck_pos, immunity_moves, timers):
    global undo_stack
    undo_stack.append(
        (
            [row[:] for row in grid],
            [duck_pos[0], duck_pos[1]],
            immunity_moves,
            timers.copy(),
        )
    )


def undo_move():
    global grid, duck_pos, immunity_moves, timers, undo_stack
    if undo_stack:
        grid, duck_pos, immunity_moves, timers = undo_stack.pop()


def draw_level_number(level_number):
    font = pygame.font.Font(None, 50)
    text = font.render(f"Level: {level_number}", True, BLACK)
    screen.blit(text, (10, 10))


def main():
    global grid, duck_pos, timers, immunity_moves, undo_stack
    welcome_screen()
    level_index = 0
    lives = 3
    grid, duck_pos = reset_level(level_index)

    level_font = pygame.font.Font(None, 36)
    lives_font = pygame.font.Font(None, 36)

    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    undo_move()
                else:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    elif event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1

                    previous_grid = [row[:] for row in grid]
                    previous_duck_pos = [duck_pos[0], duck_pos[1]]
                    previous_immunity_moves = immunity_moves
                    previous_timers = timers.copy()

                    new_pos = [duck_pos[0] + dx, duck_pos[1] + dy]
                    if 0 <= new_pos[0] < len(grid[0]) and 0 <= new_pos[1] < len(grid):
                        target_tile = grid[new_pos[1]][new_pos[0]]
                        if target_tile == LAVA and immunity_moves == 0:
                            lives -= 1
                            if lives <= 0:
                                display_message("Game Over! Back to Level 1...", RED)
                                level_index = 0
                                lives = 3
                            else:
                                display_message(f"Lost a life! {lives} remaining...", RED)
                            grid, duck_pos = reset_level(level_index)
                        elif target_tile in [EMPTY, WATER, IMMUNITY]:
                            duck_pos = new_pos
                            if target_tile == IMMUNITY:
                                immunity_moves = random.randint(7, 11)
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
                                        lives -= 1
                                        if lives <= 0:
                                            display_message("Game Over! Back to Level 1...", RED)
                                            level_index = 0
                                            lives = 3
                                        else:
                                            display_message(f"Lost a life! {lives} remaining...", RED)
                                        grid, duck_pos = reset_level(level_index)
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
                                lives = 3
                                if level_index < len(LEVELS):
                                    grid, duck_pos = reset_level(level_index)
                                else:
                                    display_message("You Win!", GREEN)
                                    running = False

                        elif target_tile == TELEPORT:
                            if (new_pos[0], new_pos[1]) in teleporters:
                                duck_pos = list(teleporters[(new_pos[0], new_pos[1])])

                    if grid != previous_grid or duck_pos != previous_duck_pos:
                        save_state(
                            previous_grid,
                            previous_duck_pos,
                            previous_immunity_moves,
                            previous_timers,
                        )
                        grid = spread_tiles(grid)

                    update_timers(grid)
                    if not is_duck_valid(grid, duck_pos):
                        lives-=1
                        if lives <= 0:
                            display_message("Game Over! Back to Level 1...", RED)
                            level_index = 0
                            lives = 3
                        else:
                            display_message(f"Lost a life! {lives} remaining...", RED)
                        grid, duck_pos = reset_level(level_index)

        draw_grid(grid)

        grid_width = len(grid[0]) * TILE_SIZE
        grid_height = len(grid) * TILE_SIZE
        offset_x = (SCREEN_WIDTH - grid_width) // 2
        offset_y = (SCREEN_HEIGHT - grid_height) // 2

        screen.blit(
            DUCK_IMG,
            (duck_pos[0] * TILE_SIZE + offset_x, duck_pos[1] * TILE_SIZE + offset_y),
        )

        level_text = level_font.render(f"Level: {level_index + 1}", True, WHITE)
        screen.blit(level_text, (10, 10))

        for i in range(lives):
            screen.blit(HEART_IMG, (SCREEN_WIDTH - 200 + i * 50, 50))

        if immunity_moves > 0:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Immunity: {immunity_moves} moves", True, GREEN)
            screen.blit(text, (SCREEN_WIDTH - 200, 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
