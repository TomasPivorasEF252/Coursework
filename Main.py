import random

GRID_SIZE = 10
MINE_COUNT = 20
HISTORY_FILE = "game_history.txt"


class BoardItem:
    def display(self):
        return "."


class Cell(BoardItem):
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        if self.is_flagged:
            return False
        self.is_revealed = True
        return True

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def display(self):
        if self.is_revealed:
            if self.is_mine:
                return "x"
            if self.adjacent_mines == 0:
                return " "
            return str(self.adjacent_mines)
        if self.is_flagged:
            return "F"
        return "."


class Grid:
    def __init__(self, size=GRID_SIZE, mine_count=MINE_COUNT):
        self.size = size
        self.mine_count = mine_count
        self.cells = [
            [Cell() for _ in range(self.size)] for _ in range(self.size)
        ]
        self.mines_placed = False

    def place_mines(self, safe_x=None, safe_y=None):
        forbidden = set()

        for row in self.cells:
            for cell in row:
                cell.is_mine = False
                cell.adjacent_mines = 0

        if safe_x is not None and safe_y is not None:
            for y in range(safe_y - 1, safe_y + 2):
                for x in range(safe_x - 1, safe_x + 2):
                    if 0 <= x < self.size and 0 <= y < self.size:
                        forbidden.add((x, y))

        positions = []
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) not in forbidden:
                    positions.append((x, y))

        if self.mine_count > len(positions):
            raise ValueError("Too many mines for the available cells.")

        random.shuffle(positions)
        for x, y in positions[:self.mine_count]:
            self.cells[y][x].is_mine = True

        self.mines_placed = True
        self.compute_adjacency()

    def ensure_safe_first_move(self, x, y):
        if not self.mines_placed:
            self.place_mines(x, y)

    def compute_adjacency(self):
        for y in range(self.size):
            for x in range(self.size):
                cell = self.cells[y][x]
                if cell.is_mine:
                    continue

                mines = 0
                for ny in range(max(0, y - 1), min(self.size, y + 2)):
                    for nx in range(max(0, x - 1), min(self.size, x + 2)):
                        if self.cells[ny][nx].is_mine:
                            mines += 1
                cell.adjacent_mines = mines

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

    def reveal_cell(self, x, y):
        cell = self.cells[y][x]

        if cell.is_revealed or cell.is_flagged:
            return "safe"

        self.ensure_safe_first_move(x, y)
        cell = self.cells[y][x]

        if cell.is_mine:
            cell.reveal()
            return "mine"
        if cell.adjacent_mines == 0:
            self.reveal_empty_area(x, y)
        else:
            cell.reveal()
        return "safe"


class Game:
    def __init__(self, player_name):
        self.player_name = player_name.strip() or "Player"
        self.grid = Grid()
        self.game_over = False
        self.score = 0
        self.result = ""

    def process_input(self, user_input):
        parts = user_input.strip().split()
        if len(parts) != 3 or parts[0] not in ("D", "F"):
            print("Invalid input")
            return False

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            print("Invalid input")
            return False

        if not (0 <= x < self.grid.size and 0 <= y < self.grid.size):
            print("Invalid input")
            return False

        if parts[0] == "F":
            self.grid.cells[y][x].toggle_flag()
            self.check_win_loss()
            return True

        result = self.grid.reveal_cell(x, y)
        if result == "mine":
            self.game_over = True
            self.result = "loss"

        self.check_win_loss()
        return True

    def check_win_loss(self):
        correct_flags = 0
        total_flags = 0

        for row in self.grid.cells:
            for cell in row:
                if cell.is_flagged:
                    total_flags += 1
                    if cell.is_mine:
                        correct_flags += 1

        self.score = correct_flags

        if not self.game_over and self.grid.mines_placed:
            if (
                correct_flags == self.grid.mine_count
                and total_flags == self.grid.mine_count
            ):
                self.game_over = True
                self.result = "win"

    def print_grid(self):
        print("  " + " ".join(str(i) for i in range(self.grid.size)))
        for y, row in enumerate(self.grid.cells):
            symbols = [cell.display() for cell in row]
            print(f"{y} " + " ".join(symbols))


class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setup(self):
        history = self.load_history()
        if history:
            print(f"Completed games in history: {len(history)}")
        player_name = input("Enter username: ")
        return Game(player_name)

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def save_result(self, game):
        record = (
            f"{game.player_name}, {game.grid.size}x{game.grid.size}, "
            f"{game.grid.mine_count}, {game.score}, {game.result}\n"
        )
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(record)

    def loop(self):
        game = self.setup()
        game.print_grid()

        while not game.game_over:
            user_input = input("Enter move (D x y or F x y): ")
            if game.process_input(user_input):
                game.print_grid()

        print(f"Username: {game.player_name}")
        print(f"Score: {game.score}")
        self.save_result(game)


if __name__ == "__main__":
    GameManager().loop()
