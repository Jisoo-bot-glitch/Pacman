class Cofig:
    highscore_filename: str = 'highscore.json'
    levels: list[int] = [10,20]
    width: int = 1120
    height: int = 800
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: float = 90
    timer: float = 10000
    player_speed: float = 0.6
    ghost_speed: float = 0.5
    scared_ghost_speed: float = 0.3
    ghost_respawn_time: float = 0.3
