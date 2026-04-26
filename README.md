# Terminal Minesweeper Report

## Introduction

### Description

This project is a terminal Minesweeper game written in Python. The game uses a fixed 10x10 board with 20 mines. The player enters a username, then uses simple text commands to reveal or flag cells until the game is won or lost. Players score is saved in a .TXT file

### Instructions to run the program

Python must be installed on the machine you are trying to run this program on.

1.Open terminal on your machine
2.Type in these commanands

To run the game:

```bash
python Main.py
```

To run the tests:

```bash
python -m unittest test_main.py
```

## Commands and rules

The player selects a cell with coordinate commands (Explained below). After the player selecs their first cell surounding ones become visible ,they are revealed to be empty or contain a number between 1 and 8. The number tells how many mines are surounding that cell. Visual below
[For this example x-are mines]

x x x
x 4 .
. . .

There are 4 mines surrounding the cell

. . .
. 4 .
. . .

How it can be shown while playing. By knowing the number and crossreffrencing with numbers nearby you can deduct where the mines are and Flag them.The game is won when all the mines are marked correctlly.

//Commands that can be used while playing

Reveal a cell:
```text
D x y
```
Flag a cell:
```text
F x y
```
Examples:
```text
D 6 7
F 3 1
```
If the input is wrong, the program prints:
```text
Invalid input
```

## Analysis

### Implementation

The program uses four main classes:

1.Cell stores the state of a single tile (mine, revealed, flagged, adjacent mines).
2.Grid manages the board, including mine placement and number calculation.
3.Game processes user input, tracks score, and checks win or loss conditions.
4.GameManager starts the game and handles saving results.

Mines are only placed after the first move has been selected.
This ensures that the player doesn't end the gme on the first move

```python
def ensure_safe_first_move(self, x, y):
    if not self.mines_placed:
        self.place_mines(x, y)
```

The selected cell and nearby cells are excluded from the mine placement.

```python
for y in range(safe_y - 1, safe_y + 2):
    for x in range(safe_x - 1, safe_x + 2):
        if 0 <= x < self.size and 0 <= y < self.size:
            forbidden.add((x, y))
```

This guarantees a safe starting area.

When the first cell has been selected nearby ones (it's neighbours are also revealed as empty),until a cell that has mines as neighbours is found, then a number is placed indicating how many of it's neighbours are mines.

```python
def reveal_empty_area(self, x, y):
    cell = self.cells[y][x]

    if cell.is_mine or cell.is_flagged or cell.is_revealed:
        return

    cell.reveal()
    if cell.adjacent_mines != 0:
        return

    for ny in range(max(0, y - 1), min(self.size, y + 2)):
        for nx in range(max(0, x - 1), min(self.size, x + 2)):
            if nx == x and ny == y:
                continue
            self.reveal_empty_area(nx, ny)
```

Player input validation before executing the player given inputs

```python
if len(parts) != 3 or parts[0] not in ("D", "F"):
    print("Invalid input")
```

Number of saved scores is printed before every game if such scores exist.
And after every game the score is saved in the .TXT file as a new line. 

### OOP Principles

Encapsulation: cell data is controlled through methods like reveal() and toggle_flag().
Abstraction: each class has a clear and separate responsibility.
Inheritance: Cell inherits from BoardItem.
Polymorphism: Cell.display() overrides the base method to show correct symbols.

### Design Pattern

The Singleton pattern is used in GameManager. So only one instance of the game manager could exist per session. If not for this desighn pattern there could be multiple games running in the same instance. Unclear control of what grid is being played on ETC... That's why Singleton was used in this project

### Composition and Aggregation

Composition: Grid is composed of many Cell objects.
Aggregation: Game uses a Grid, but the grid exists independently.

### Testing

Unit tests are implemented using the unittest framework.

They verify:

1.correct grid size and mine count
2.correct mine placement
3.safe first move behavior
4.recursive reveal of empty areas
5.input validation
6.win condition (all mines flagged)
7.loss condition (mine revealed)

## Results

The game runs correctly ,using simple terminal commands. The first move selected by the player is always safe ,program expands the starting area automatically and places numbers where they are needed. Invalid input is correctly rejected. Game scores are saved in a .TXT file. Core functionality is tested with the seperate test_main.py file. 

## Conclusions

The project achieves its main goal: a working terminal Minesweeper game with clear Python code, basic OOP structure, saved results, and unit tests.

The program is written so it could be easilly expanded in functionality in the future. Main additions could be a GUI ,Grid size and mine count selection based on the selected difficulty. An actual flood fill algorithm after the first cell is selected
