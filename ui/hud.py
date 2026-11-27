"""Draw the HUD bar above the maze: score, lives, level, time and title."""

import pygame

from game.session import Session
from ui.game_view import HUD_HEIGHT, MARGIN

TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 215, 0)
COLUMN2_X = 170
ROW1_Y = 12
ROW2_Y = 38


def draw_hud(screen: pygame.Surface, session: Session,
             font: pygame.font.Font, title_font: pygame.font.Font) -> None:
    """Draw score, lives, level and time on the left, and a big title.

    Args:
        screen: The window surface to draw on.
        session: Score, lives, level and time left of the game.
        font: Small font for the four values.
        title_font: Big font for the title.
    """
    score = font.render(f"Score: {session.score}", True, TEXT_COLOR)
    screen.blit(score, (MARGIN, ROW1_Y))

    lives = font.render(f"Lives: {session.lives}", True, TEXT_COLOR)
    screen.blit(lives, (MARGIN, ROW2_Y))

    level = font.render(f"Level: {session.level}", True, TEXT_COLOR)
    screen.blit(level, (COLUMN2_X, ROW1_Y))

    time = font.render(f"Time: {int(session.time_left)}", True, TEXT_COLOR)
    screen.blit(time, (COLUMN2_X, ROW2_Y))

    title = title_font.render("Chataigne_Pacman", True, TITLE_COLOR)
    x = screen.get_width() - MARGIN - title.get_width()
    y = (MARGIN + HUD_HEIGHT - title.get_height()) // 2
    screen.blit(title, (x, y))
