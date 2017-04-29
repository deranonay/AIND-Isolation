"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    @unittest.skip
    def test_depth2(self):
        expected = [((5, 7), (4, 9)), ((9, 7), (4, 9)), ((9, 7), (0, 7)), ((8, 8), (0, 7)), ((8, 8), (1, 10)), ((8, 4), (0, 9)), ((9, 7), (1, 10)), ((9, 7), (4, 7)), ((9, 7), (1, 6)), ((5, 7), (0, 9)), ((9, 7), (3, 10)), ((6, 4), (0, 9)), ((9, 5), (4, 9)), ((9, 5), (0, 9)), ((8, 8), (4, 7)), ((9, 5), (0, 7)), ((8, 8), (1, 6)), ((8, 4), (4, 9)), ((8, 4), (0, 7)), ((8, 8), (4, 9)), ((8, 8), (0, 9)), ((9, 7), (0, 9)), ((5, 7), (1, 6)), ((8, 4), (1, 10)), ((8, 4), (4, 7)), ((5, 7), (1, 10)), ((8, 4), (1, 6)), ((6, 4), (3, 10)), ((9, 5), (1, 6)), ((9, 5), (4, 7)), ((8, 4), (3, 10)), ((6, 4), (1, 6)), ((6, 4), (4, 7)), ((9, 5), (3, 10)), ((5, 7), (3, 10)), ((6, 4), (1, 10)), ((5, 7), (4, 7)), ((9, 5), (1, 10)), ((6, 4), (0, 7)), ((6, 4), (4, 9)), ((5, 7), (0, 7)), ((8, 8), (3, 10))]
        actual = [((5, 7), (4, 9)), ((9, 7), (4, 9)), ((9, 7), (0, 7)), ((8, 8), (0, 7)), ((8, 8), (1, 10)), ((8, 4), (0, 9)), ((9, 7), (1, 10)), ((9, 7), (4, 7)), ((6, 4), (2, 8)), ((5, 7), (0, 9)), ((9, 7), (1, 6)), ((9, 7), (3, 10)), ((6, 4), (0, 9)), ((9, 5), (4, 9)), ((9, 7), (2, 8)), ((9, 5), (0, 9)), ((5, 7), (2, 8)), ((8, 8), (4, 7)), ((9, 5), (0, 7)), ((8, 8), (1, 6)), ((8, 8), (2, 8)), ((8, 4), (4, 9)), ((8, 4), (0, 7)), ((8, 8), (4, 9)), ((8, 8), (0, 9)), ((5, 7), (1, 6)), ((8, 4), (1, 10)), ((8, 4), (4, 7)), ((9, 7), (0, 9)), ((8, 4), (1, 6)), ((5, 7), (1, 10)), ((6, 4), (3, 10)), ((9, 5), (1, 6)), ((9, 5), (4, 7)), ((9, 5), (2, 8)), ((8, 4), (3, 10)), ((6, 4), (1, 6)), ((6, 4), (4, 7)), ((9, 5), (3, 10)), ((5, 7), (3, 10)), ((6, 4), (1, 10)), ((8, 4), (2, 8)), ((5, 7), (4, 7)), ((9, 5), (1, 10)), ((6, 4), (0, 7)), ((6, 4), (4, 9)), ((5, 7), (0, 7)), ((8, 8), (3, 10))]
        diff = set(actual) - set(expected)
        print(diff)
        self.assertTrue(len(diff) == 0, "extra leaf nodes found")

    @unittest.skip
    def test_move_depth2_1(self):
        depth = 2
        visited_moves = [(2, 1), (2, 4), (2, 5), (2, 6), (3, 2), (3, 3), (3, 8), (4, 5), (4, 6), (5, 3), (5, 5), (5, 6),
                         (6, 3), (6, 5), (6, 6), (7, 5), (7, 7), (7, 8), (8, 5), (8, 6), (7, 3), (7, 2)]
        next_move = self.get_next_move(11, depth, visited_moves)
        self.assertTrue(next_move == (5, 2))

    @unittest.skip
    def test_move_depth2_2(self):
        depth = 2
        visited_moves = [(1, 2), (2, 7), (2, 8), (3, 3), (3, 5), (3, 6), (4, 6), (5, 2), (5, 7), (6, 3), (6, 4), (6, 5),
                         (6, 6), (7, 2), (7, 4), (7, 5), (7, 8), (8, 4), (8, 6), (8, 7), (4, 7), (2, 3)]
        next_move = self.get_next_move(11, depth, visited_moves)
        self.assertTrue(next_move == (2, 6))

    def test_move_depth2_3(self):
        depth = 2
        visited_moves = [(2, 1), (2, 2), (2, 4), (2, 6), (3, 2), (3, 3), (3, 4), (3, 8), (4, 2), (4, 3), (4, 4), (4, 7),
                         (5, 2), (5, 7), (6, 7), (6, 8), (7, 5), (7, 8), (8, 6), (8, 7), (1, 7), (2, 3)]
        next_move = self.get_next_move(11, depth, visited_moves)
        self.assertTrue(next_move == (2, 9))

    def get_next_move(self, board_size, depth, visited_moves):
        player1 = game_agent.MinimaxPlayer(depth)
        player2 = game_agent.MinimaxPlayer(depth)
        self.game = isolation.Board(player1, player2, board_size, board_size)

        for move in visited_moves:
            print('Applying move {}'.format(move))
            self.game.apply_move(move)
        print(self.game.print_board())
        next_move = player1.get_move(self.game, lambda: 100000)
        self.game.apply_move(next_move)
        print(self.game.print_board())
        return next_move


if __name__ == '__main__':
    unittest.main()
