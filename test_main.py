import io
import unittest
from contextlib import redirect_stdout

from Main import Game
from Main import Grid


class GridTests(unittest.TestCase):
    def test_grid_is_created_with_expected_size(self):
        grid = Grid()

        self.assertEqual(grid.size, 10)
        self.assertEqual(grid.mine_count, 20)
        self.assertEqual(len(grid.cells), 10)
        self.assertEqual(len(grid.cells[0]), 10)

    def test_mine_placement_uses_requested_count(self):
        grid = Grid()
        grid.place_mines(0, 0)

        mine_total = sum(cell.is_mine for row in grid.cells for cell in row)
        self.assertEqual(mine_total, 20)

    def test_first_reveal_is_safe(self):
        grid = Grid()
        result = grid.reveal_cell(5, 5)
        cell = grid.cells[5][5]

        self.assertEqual(result, "safe")
        self.assertTrue(cell.is_revealed)
        self.assertFalse(cell.is_mine)

    def test_reveal_expands_through_connected_empty_cells(self):
        grid = Grid(size=3, mine_count=1)
        grid.cells[2][2].is_mine = True
        grid.mines_placed = True
        grid.compute_adjacency()

        result = grid.reveal_cell(0, 0)

        self.assertEqual(result, "safe")
        revealed_safe_cells = sum(
            cell.is_revealed and not cell.is_mine
            for row in grid.cells
            for cell in row
        )
        self.assertEqual(revealed_safe_cells, 8)


class GameTests(unittest.TestCase):
    def test_invalid_input_is_rejected(self):
        game = Game("Player")
        output = io.StringIO()

        with redirect_stdout(output):
            result = game.process_input("Z 1 1")

        self.assertFalse(result)
        self.assertIn("Invalid input", output.getvalue())

    def test_game_is_won_when_all_mines_are_flagged(self):
        game = Game("Alice")
        game.grid = Grid(mine_count=1)
        game.grid.cells[0][0].is_mine = True
        game.grid.mines_placed = True
        game.grid.compute_adjacency()

        game.process_input("F 0 0")

        self.assertTrue(game.game_over)
        self.assertEqual(game.result, "win")

    def test_game_is_lost_when_a_mine_is_revealed(self):
        game = Game("Bob")
        game.grid = Grid(mine_count=1)
        game.grid.cells[1][1].is_mine = True
        game.grid.mines_placed = True
        game.grid.compute_adjacency()

        game.process_input("D 1 1")

        self.assertTrue(game.game_over)
        self.assertEqual(game.result, "loss")


if __name__ == "__main__":
    unittest.main()
