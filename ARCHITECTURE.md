# Minesweeper Game Architecture

## Overview
A classic Minesweeper game with three difficulty levels (beginner, intermediate, expert), cell uncovering, mine detection, flagging mechanism, and visual feedback.

## Modules

### 1. `game_state.py` - Core Game Logic
**Responsibility**: Manages the game state, board generation, mine placement, and win/loss conditions.

**Exposed Interfaces**:
- `GameConfig`: Named tuple with (rows, cols, mines) for each difficulty
- `Difficulty`: Enum (BEGINNER, INTERMEDIATE, EXPERT)
- `GameState`: Enum (PLAYING, WON, LOST)
- `create_board(rows, cols, mines)`: Returns 2D grid with mine locations
- `count_adjacent_mines(board, row, col)`: Returns count of adjacent mines
- `initialize_game(difficulty)`: Creates new game with given difficulty

**Dependencies**: None (pure logic module)

---

### 2. `ui.py` - User Interface
**Responsibility**: Renders the game board, handles user input (clicks, flagging), and displays game messages.

**Exposed Interfaces**:
- `UI`: Class with methods:
  - `render_board(board, revealed, flagged)`: Renders current game state
  - `handle_click(x, y)`: Processes cell clicks
  - `toggle_flag(x, y)`: Toggles flag on a cell
  - `display_message(message)`: Shows game status (win/loss)
  - `get_input()`: Reads user input
- `CellState`: Enum (HIDDEN, REVEALED, FLAGGED)

**Dependencies**: `game_state.py`

---

### 3. `main.py` - Application Entry Point
**Responsibility**: Coordinates game flow, initializes game, handles difficulty selection, and runs game loop.

**Exposed Interfaces**:
- `select_difficulty()`: Prompts user for difficulty level
- `run_game()`: Main game loop

**Dependencies**: `game_state.py`, `ui.py`

---

## File Structure
```
minesweeper-classic-8559/
├── game_state.py    # Core game logic
├── ui.py            # User interface
├── main.py          # Entry point
└── README.md        # Documentation
```

## Data Structures

### Board Representation
- 2D grid (list of lists)
- Each cell: `None` (empty) or `'M'` (mine)
- Hidden cells displayed as `'#'`
- Revealed cells show mine count (0-8) or `'M'` (mine)
- Flagged cells marked with `'F'`

### Game State
- Board (2D grid)
- Revealed set (coordinates of uncovered cells)
- Flagged set (coordinates of flagged cells)
- Current difficulty
- Game status (PLAYING, WON, LOST)

## User Flow
1. Start game → Select difficulty
2. Display board (all cells hidden)
3. User clicks cell:
   - If mine: Game over
   - If empty: Reveal cell and adjacent empty cells (flood fill)
   - If number: Show count
4. User can flag cells as suspected mines
5. Continue until all non-mine cells revealed (win) or mine clicked (loss)
