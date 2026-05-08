from enum import Enum
from typing import NamedTuple
import random


class Difficulty(Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    EXPERT = "EXPERT"


class GameConfig(NamedTuple):
    rows: int
    cols: int
    mines: int


BEGINNER_CONFIG = GameConfig(rows=9, cols=9, mines=10)
INTERMEDIATE_CONFIG = GameConfig(rows=16, cols=16, mines=40)
EXPERT_CONFIG = GameConfig(rows=16, cols=30, mines=99)

DIFFICULTY_CONFIGS = {
    Difficulty.BEGINNER: BEGINNER_CONFIG,
    Difficulty.INTERMEDIATE: INTERMEDIATE_CONFIG,
    Difficulty.EXPERT: EXPERT_CONFIG,
}


class GameState(Enum):
    PLAYING = "PLAYING"
    WON = "WON"
    LOST = "LOST"


def create_board(rows: int, cols: int, mines: int) -> list[list[str | None]]:
    board = [[None for _ in range(cols)] for _ in range(rows)]
    
    mine_positions = set()
    while len(mine_positions) < mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        mine_positions.add((row, col))
    
    for row, col in mine_positions:
        board[row][col] = 'M'
    
    return board


def count_adjacent_mines(board: list[list[str | None]], row: int, col: int) -> int:
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    count = 0
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if board[new_row][new_col] == 'M':
                    count += 1
    
    return count


def initialize_game(difficulty: Difficulty) -> dict:
    config = DIFFICULTY_CONFIGS[difficulty]
    board = create_board(config.rows, config.cols, config.mines)
    
    revealed = set()
    flagged = set()
    
    for row in range(config.rows):
        for col in range(config.cols):
            if board[row][col] != 'M':
                board[row][col] = count_adjacent_mines(board, row, col)
    
    return {
        'board': board,
        'revealed': revealed,
        'flagged': flagged,
        'difficulty': difficulty,
        'state': GameState.PLAYING,
        'config': config,
    }
