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


    def test_empty(self):
        reload(game_agent)
        self.player1 = game_agent.AlphaBetaPlayer()
        self.player2 = game_agent.AlphaBetaPlayer()
        game = isolation.Board(self.player1, self.player2)
        self.assertEqual(game.get_player_location(self.player1), None)
        self.assertEqual(game.get_player_location(self.player2), None)
        game.play(time_limit=100)
        self.assertNotEqual(game.get_player_location(self.player1), None)
        self.assertNotEqual(game.get_player_location(self.player2), None)

    def test_empty(self):
    	reload(game_agent)
    	self.player1 = game_agent.MinimaxPlayer()
    	self.player2 = game_agent.MinimaxPlayer()
    	game = isolation.Board(self.player1, self.player2)
    	self.assertEqual(game.get_player_location(self.player1), None)
    	self.assertEqual(game.get_player_location(self.player2), None)
    	game.play(time_limit=100)
    	self.assertNotEqual(game.get_player_location(self.player1), None)
    	self.assertNotEqual(game.get_player_location(self.player2), None)




if __name__ == '__main__':
    unittest.main()
