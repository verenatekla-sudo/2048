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

# Initialize screen
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT + SCORE_HEIGHT))
pygame.display.set_caption('2048 Game')

# Define fonts
font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 48)

# Colors for tiles (2^1 to 2^12)
TILE_COLORS = {
    2: (255, 204, 204),     # Light pink
    4: (255, 230, 204),     # Light orange
    8: (204, 255, 204),     # Light green
    16: (204, 204, 255),    # Light blue
    32: (255, 204, 255),    # Light purple
    64: (255, 255, 204),    # Light yellow
    128: (255, 214, 153),   # Pastel orange
    256: (255, 214, 255),   # Pastel pink
    512: (204, 255, 230),   # Pastel green
    1024: (204, 204, 255),  # Pastel blue
    2048: (255, 255, 153),  # Pastel yellow
    4096: (192, 192, 192)   # Gray
}

BACKGROUND_COLOR = (169, 169, 169)  # Gray

# Initialize the grid with zeros
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0

# Helper function to draw tile
def draw_tile(x, y, value):
    if value in TILE_COLORS:
        color = TILE_COLORS[value]
    else:
        color = (0, 0, 0)

    pygame.draw.rect(
        screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    text_surface = font.render(
        str(value), True, BLACK)
    text_rect = text_surface.get_rect(
        center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
    screen.blit(text_surface, text_rect)

# Helper function to generate new tile (either 2 or 4)
def generate_new_tile():
    empty_cells = [
        (x, y) for x in range(GRID_SIZE)
        for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = 2 if random.random() < 0.9 else 4

# Function to update the screen
def update_screen():
    screen.fill(BACKGROUND_COLOR)

    # Draw the score label
    score_label = score_font.render(
        f"Score: {score}", True, BLACK)
