from enum import Enum
from typing import List, Set, Tuple


class CellState(Enum):
    HIDDEN = "HIDDEN"
    REVEALED = "REVEALED"
    FLAGGED = "FLAGGED"


class UI:
    def __init__(self) -> None:
        self._revealed: Set[Tuple[int, int]] = set()
        self._flagged: Set[Tuple[int, int]] = set()
        self._game_over: bool = False
        self._message: str = ""

    def render_board(self, board: List[List[str]], revealed: Set[Tuple[int, int]], flagged: Set[Tuple[int, int]]) -> None:
        self._revealed = revealed
        self._flagged = flagged
        
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        print("\n  ", end="")
        for col in range(cols):
            print(f" {col} ", end="")
        print()
        
        print("  ", end="")
        for col in range(cols):
            print("---", end="")
        print()
        
        for row in range(rows):
            print(f"{row}|", end="")
            for col in range(cols):
                if (row, col) in self._flagged:
                    print(" F |", end="")
                elif (row, col) in self._revealed:
                    cell = board[row][col]
                    if cell == 'M':
                        print(" M |", end="")
                    else:
                        print(f" {cell} |", end="")
                else:
                    print(" # |", end="")
            print()
            print("  ", end="")
            for col in range(cols):
                print("---", end="")
            print()
        
        if self._message and not self._game_over:
            print(f"\n{self._message}")
            self._message = ""

    def handle_click(self, x: int, y: int) -> str:
        return f"CLICK:{x},{y}"

    def toggle_flag(self, x: int, y: int) -> str:
        return f"FLAG:{x},{y}"

    def display_message(self, message: str) -> None:
        self._message = message
        print(f"\n{message}")

    def get_input(self) -> str:
        return input("> ")
