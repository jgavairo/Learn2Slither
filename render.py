import pygame

# Colors
BG_COLOR = (18, 18, 18)
GRID_COLOR = (35, 35, 35)
SNAKE_HEAD_COLOR = (80, 180, 255)
SNAKE_BODY_COLOR = (40, 140, 200)
FOOD_GREEN_COLOR = (90, 200, 90)
FOOD_RED_COLOR = (220, 70, 70)


def ensure_screen(size: int, cell_size: int = 32):
    """Create a pygame display surface sized to the board."""
    width = size * cell_size
    height = size * cell_size
    return pygame.display.set_mode((width, height))


def render(board, screen, cell_size: int = 32, draw_grid: bool = True):
    """
    Render the current board state onto the provided pygame screen.
    Call inside your game loop after board.update().
    """
    size = board.get_size()
    screen.fill(BG_COLOR)

    if draw_grid:
        for i in range(size + 1):
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (i * cell_size, 0),
                (i * cell_size, size * cell_size),
            )
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (0, i * cell_size),
                (size * cell_size, i * cell_size),
            )

    # Draw food
    for food in board.get_food():
        fx, fy = food.get_position()
        color = (
            FOOD_GREEN_COLOR if food.get_color() == "GREEN" else FOOD_RED_COLOR
        )
        rect = pygame.Rect(
            fx * cell_size, fy * cell_size, cell_size, cell_size)
        pygame.draw.circle(screen, color, rect.center, cell_size // 3)

    # Draw snake
    snake = board.get_snake()
    if snake:
        for i, (sx, sy) in enumerate(snake.get_body()):
            rect = pygame.Rect(
                sx * cell_size, sy * cell_size, cell_size, cell_size
            )
            if i == 0:
                pygame.draw.rect(
                    screen, SNAKE_HEAD_COLOR, rect, border_radius=6
                )
            else:
                pygame.draw.rect(
                    screen, SNAKE_BODY_COLOR, rect, border_radius=6
                )

    pygame.display.flip()
