"""
Minesweeper Game - Main Entry Point
Coordinates game flow, difficulty selection, and user interaction.
"""

from game_state import (
    Difficulty, 
    GameState, 
    initialize_game, 
    count_adjacent_mines,
    BEGINNER_CONFIG,
    INTERMEDIATE_CONFIG,
    EXPERT_CONFIG
)
from ui import UI


def select_difficulty() -> Difficulty:
    """Prompt user to select a difficulty level."""
    print("\n=== Minesweeper Classic ===")
    print("Select difficulty level:")
    print("  1. Beginner (9x9, 10 mines)")
    print("  2. Intermediate (16x16, 40 mines)")
    print("  3. Expert (16x30, 99 mines)")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            return Difficulty.BEGINNER
        elif choice == "2":
            return Difficulty.INTERMEDIATE
        elif choice == "3":
            return Difficulty.EXPERT
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def reveal_cell(game: dict, x: int, y: int) -> bool:
    """
    Reveal a cell and handle game logic.
    Returns True if game should continue, False if game ended.
    """
    board = game['board']
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    # Validate coordinates
    if x < 0 or x >= cols or y < 0 or y >= rows:
        print(f"Invalid coordinates. Enter values between 0-{cols-1} and 0-{rows-1}.")
        return True
    
    # Check if already revealed or flagged
    if (y, x) in game['revealed']:
        print("Cell already revealed.")
        return True
    if (y, x) in game['flagged']:
        print("Cell is flagged. Remove flag first.")
        return True
    
    cell_value = board[y][x]
    game['revealed'].add((y, x))
    
    # Hit a mine
    if cell_value == 'M':
        game['state'] = GameState.LOST
        return False
    
    # Empty cell - reveal adjacent cells (flood fill)
    if cell_value == 0:
        reveal_adjacent(game, y, x)
    
    # Check for win
    if check_win(game):
        game['state'] = GameState.WON
        return False
    
    return True


def reveal_adjacent(game: dict, row: int, col: int) -> None:
    """Recursively reveal empty cells (flood fill)."""
    board = game['board']
    revealed = game['revealed']
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if (new_row, new_col) not in revealed:
                    cell_value = board[new_row][new_col]
                    if cell_value != 'M':
                        revealed.add((new_row, new_col))
                        if cell_value == 0:
                            reveal_adjacent(game, new_row, new_col)


def check_win(game: dict) -> bool:
    """Check if the player has won the game."""
    config = game['config']
    total_cells = config.rows * config.cols
    revealed_count = len(game['revealed'])
    mine_count = config.mines
    return revealed_count == (total_cells - mine_count)


def toggle_flag(game: dict, x: int, y: int) -> bool:
    """Toggle a flag on a cell."""
    board = game['board']
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    # Validate coordinates
    if x < 0 or x >= cols or y < 0 or y >= rows:
        print(f"Invalid coordinates. Enter values between 0-{cols-1} and 0-{rows-1}.")
        return True
    
    # Check if already revealed
    if (y, x) in game['revealed']:
        print("Cell already revealed. Cannot flag.")
        return True
    
    if (y, x) in game['flagged']:
        game['flagged'].remove((y, x))
    else:
        game['flagged'].add((y, x))
    
    return True


def display_final_board(game: dict, ui: UI) -> None:
    """Display the board with all mines revealed at game end."""
    board = game['board']
    revealed = game['revealed'].copy()
    
    # Reveal all mines
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'M':
                revealed.add((row, col))
    
    ui.render_board(board, revealed, game['flagged'])


def run_game() -> None:
    """Main game loop."""
    ui = UI()
    
    while True:
        # Select difficulty and initialize game
        difficulty = select_difficulty()
        game = initialize_game(difficulty)
        ui.render_board(game['board'], game['revealed'], game['flagged'])
        
        print("\nCommands:")
        print("  click x,y  - Reveal cell at (x, y)")
        print("  flag x,y   - Toggle flag at (x, y)")
        print("  quit       - Exit game")
        print()
        
        # Game loop
        while game['state'] == GameState.PLAYING:
            command = ui.get_input().strip().lower()
            
            if command == 'quit':
                print("Thanks for playing!")
                return
            
            # Parse command
            parts = command.replace(',', ' ').split()
            
            if len(parts) >= 2:
                try:
                    x = int(parts[-2])
                    y = int(parts[-1])
                    
                    if parts[0] == 'flag':
                        if not toggle_flag(game, x, y):
                            display_final_board(game, ui)
                            if game['state'] == GameState.WON:
                                ui.display_message("Congratulations! You won!")
                            else:
                                ui.display_message("Game Over! You hit a mine!")
                            break
                    else:
                        if not reveal_cell(game, x, y):
                            display_final_board(game, ui)
                            if game['state'] == GameState.WON:
                                ui.display_message("Congratulations! You won!")
                            else:
                                ui.display_message("Game Over! You hit a mine!")
                            break
                except ValueError:
                    print("Invalid input. Use format: 'click x,y' or 'flag x,y'")
            else:
                print("Invalid command. Try again.")
            
            ui.render_board(game['board'], game['revealed'], game['flagged'])
        
        # Ask to play again
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing Minesweeper Classic!")
            break


def main() -> None:
    """Entry point for the Minesweeper game."""
    run_game()


if __name__ == '__main__':
    main()
