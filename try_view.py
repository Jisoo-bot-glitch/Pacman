"""Temporary demo: draws game_view with fake data. Delete when app.py works."""
import pygame
from mazegenerator import MazeGenerator

from game.ghost import Ghost
from game.grid import Position
from ui.sprites import load_sprites
from ui.game_view import window_size, draw


class FakePlayer:
    """Stands in for Elvira's Player until it exists."""

    def __init__(self, pos: Position) -> None:
        self.pos = pos


class FakeGame:
    """Stands in for Elvira's Game: only what draw() needs."""

    def __init__(self, maze: list[list[int]], player: FakePlayer,
                 ghosts: list[Ghost], pacgums: set[Position],
                 super_pacgums: set[Position]) -> None:
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums


pygame.init()
maze = MazeGenerator(size=(20, 20), seed=42).maze

window = window_size(maze)
screen = pygame.display.set_mode(window)
sprites = load_sprites()
running = True
clock = pygame.time.Clock()
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
game = FakeGame(maze, FakePlayer(pos), ghosts, pacgums, super_pacgums)

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for ghost in game.ghosts:
        ghost.update(game.maze, game.player.pos, dt)
    draw(screen, game, sprites)
    pygame.display.flip()

pygame.quit()
