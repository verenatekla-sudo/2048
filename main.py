import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
SCORE_HEIGHT = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

screen = pygame.display.set_mode((WIDTH, HEIGHT + SCORE_HEIGHT))
pygame.display.set_caption("2048 Game")

font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 48)

TILE_COLORS = {
    2: (255, 204, 204),
    4: (255, 230, 204),
    8: (204, 255, 204),
    16: (204, 204, 255),
    32: (255, 204, 255),
    64: (255, 255, 204),
    128: (255, 214, 153),
    256: (255, 214, 255),
    512: (204, 255, 230),
    1024: (204, 204, 255),
    2048: (255, 255, 153),
    4096: (192, 192, 192)
}

BACKGROUND_COLOR = GRAY

grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0


# ----------------------------
# DRAW FUNCTIONS
# ----------------------------

def draw_tile(x, y, value):
    color = TILE_COLORS.get(value, (60, 60, 60))
    pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

    if value != 0:
        text_surface = font.render(str(value), True, BLACK)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text_surface, text_rect)


def update_screen():
    screen.fill(BACKGROUND_COLOR)

    # score
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT + SCORE_HEIGHT // 2))
    screen.blit(score_text, score_rect)

    # grid
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            draw_tile(c * TILE_SIZE, r * TILE_SIZE, grid[r][c])

    pygame.display.flip()


# ----------------------------
# GRID LOGIC
# ----------------------------

def generate_new_tile():
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2 if random.random() < 0.9 else 4


def compress(row):
    new = [x for x in row if x != 0]
    new += [0] * (GRID_SIZE - len(new))
    return new


def merge(row):
    global score
    for i in range(GRID_SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row


def move_left():
    changed = False
    new_grid = []

    for r in range(GRID_SIZE):
        row = grid[r]
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        new_grid.append(final)
        if final != row:
            changed = True

    return new_grid, changed


def move_right():
    reversed_grid = [row[::-1] for row in grid]
    new, changed = move_left_grid(reversed_grid)
    new = [row[::-1] for row in new]
    return new, changed


def move_left_grid(g):
    """move_left but using custom grid (helper for right/down)"""
    changed = False
    new_grid = []

    for r in range(GRID_SIZE):
        row = g[r]
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        new_grid.append(final)
        if final != row:
            changed = True
    return new_grid, changed


def move_up():
    transposed = list(map(list, zip(*grid)))
    new, changed = move_left_grid(transposed)
    new = list(map(list, zip(*new)))
    return new, changed


def move_down():
    transposed = list(map(list, zip(*grid)))
    reversed_grid = [row[::-1] for row in transposed]
    new, changed = move_left_grid(reversed_grid)
    new = [row[::-1] for row in new]
    new = list(map(list, zip(*new)))
    return new, changed


def can_move():
    if any(0 in row for row in grid):
        return True

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1]:
                return True

    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r + 1][c]:
                return True

    return False


def game_over():
    text = font.render("GAME OVER", True, WHITE, BLACK)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.delay(2000)


# ----------------------------
# INIT
# ----------------------------

generate_new_tile()
generate_new_tile()
update_screen()

running = True

# ----------------------------
# MAIN LOOP
# ----------------------------

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            moved = False

            if event.key == pygame.K_LEFT:
                new, moved = move_left()
            elif event.key == pygame.K_RIGHT:
                new, moved = move_right()
            elif event.key == pygame.K_UP:
                new, moved = move_up()
            elif event.key == pygame.K_DOWN:
                new, moved = move_down()
            else:
                continue

            if moved:
                grid = new
                generate_new_tile()
                update_screen()

            if any(2048 in row for row in grid):
                game_over()
                running = False

            if not can_move():
                game_over()
                running = False

pygame.quit()
