"""Temporary demo: draws game_view with fake data. Delete when app.py works."""
import pygame
from mazegenerator import MazeGenerator

from game.ghost import Ghost
from game.ghost_ai import next_step
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
pos = (10, 15)
last_x = len(maze[0]) - 1
last_y = len(maze) - 1
ghosts = [
    Ghost("red", (0, 0)),
    Ghost("pink", (0, last_y)),
    Ghost("cyan", (last_x, 0)),
    Ghost("orange", (last_x, last_y))
]
pacgums = {(0, 1), (0, 2), (0, 3), (0,  4),
           (0, 5), (2, 1), (3, 1), (4, 1), (5, 1), (16, 5),
           (16, 2), (16, 3), (17, 1), (17, 2), (17, 3)}
super_pacgums = {(1, 0), (0, 16), (18, 18), (17, 0)}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for ghost in ghosts:
                ghost.pos = next_step(maze, ghost.pos, pos)

    screen.fill(BACKGROUND_COLOR)
    draw_maze(screen, maze, sprites)
    draw_pacgums(screen, pacgums, super_pacgums, sprites)
    draw_ghosts(screen, ghosts, sprites)
    draw_player(screen, pos, sprites)
    pygame.display.flip()

pygame.quit()
