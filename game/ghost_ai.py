"""Ghost movement: BFS chase toward a target cell."""

from collections import deque

from game.grid import can_move, N, E, S, W, Position

DIRECTIONS = {
    N: (0, -1),
    E: (1, 0),
    W: (-1, 0),
    S: (0, 1)
}


def neighbors(maze: list[list[int]], pos: tuple[int, int]) -> list[Position]:
    """Return the cells next to pos with no wall in between.

    Directions are checked in the order N, E, S, W.

    Args:
        maze: The maze grid, read as maze[y][x].
        pos: The cell to look around, as (x, y).

    Returns:
        The open neighbor cells.
    """
    x, y = pos
    possible = []
    for direction, (dx, dy) in DIRECTIONS.items():
        if can_move(maze, x, y, direction):
            possible.append((x + dx, y + dy))

    return possible


def next_step(maze: list[list[int]], start: Position,
              target: Position) -> Position:
    """Return the next cell on a shortest path from start to target.

    Uses BFS from start. Only the first step is returned, because the
    target (the player) keeps moving, so the path is computed again
    every time the ghost moves.

    Args:
        maze: The maze grid, read as maze[y][x].
        start: The ghost's cell.
        target: The cell to reach (the player, or any other cell).

    Returns:
        The next cell to move to. If start is target, or the target
        cannot be reached, returns start (the ghost stays).
    """
    if start == target:
        return start

    q: deque[Position] = deque([start])
    visited: set[Position] = {start}
    parents: dict[Position, Position] = {}

    while q:
        cell = q.popleft()
        if cell == target:
            break
        for possible in neighbors(maze, cell):
            if possible not in visited:
                visited.add(possible)
                q.append(possible)
                parents[possible] = cell

    if target not in parents:
        return start

    cell = target
    while parents[cell] != start:
        cell = parents[cell]
    return cell
