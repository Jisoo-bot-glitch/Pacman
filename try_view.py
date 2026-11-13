"""Temporary demo: draws game_view with fake data. Delete when app.py works."""
import pygame
from mazegenerator import MazeGenerator

from game.ghost import Ghost
from ui.sprites import load_sprites
from ui.game_view import (window_size, draw_pacgums,
                          draw_maze, draw_player, draw_ghosts,
                          BACKGROUND_COLOR)


pygame.init()
maze = MazeGenerator(size=(20, 20), seed=42).maze

window = window_size(maze)
screen = pygame.display.set_mode(window)
sprites = load_sprites()
running = True
pos = (1, 1)
ghosts = [
    Ghost("red", (17, 0)),
    Ghost("pink", (0, 16)),
    Ghost("cyan", (18, 18)),
    Ghost("orange", (15, 15))
]
pacgums = {(0, 1), (0, 2), (0, 3), (0,  4),
           (0, 5), (2, 1), (3, 1), (4, 1), (5, 1), (16, 5),
           (16, 2), (16, 3), (17, 1), (17, 2), (17, 3)}
super_pacgums = {(0, 0), (19, 0), (0, 19), (19, 19)}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BACKGROUND_COLOR)
    draw_maze(screen, maze, sprites)
    draw_pacgums(screen, pacgums, super_pacgums, sprites)
    draw_ghosts(screen, ghosts, sprites)
    draw_player(screen, pos, sprites)
    pygame.display.flip()

pygame.quit()
