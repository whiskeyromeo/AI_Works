"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def time_check(self):
    '''
        Checks the state of the timer, raising a Timeout if needed
    '''
    if self.time_left() < self.TIMER_THRESHOLD:
        raise SearchTimeout()

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic
    This measures the difference between the sum of the diagonal distances
    for each available move to a player relative to their opponents location
    and the sum of diagonal distances for each available move for an opponent
    relative to the players location

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    #USES A SUM OF DIFFERENCE IN DIAGONAL DISTANCES BETWEEN PLAYERS
    # CURRENT LOCATION AND THE MOVES AVAILABLE

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(game.get_opponent(player))

    own_diag_dist = 0.0

    for move in own_moves:
        py_dist = math.sqrt((move[1]-opp_location[1])**2 + (move[0]-opp_location[0])**2)
        own_diag_dist += py_dist

    if len(own_moves) > 0:
        own_diag_dist = own_diag_dist/len(own_moves)

    opp_diag_dist = 0.0

    for move in opp_moves:
        py_dist = math.sqrt((move[1]-own_location[1])**2 + (move[0]-own_location[0])**2)
        opp_diag_dist += py_dist
        
    if len(opp_moves) > 0:
        opp_diag_dist = opp_diag_dist/len(opp_moves)

    return float(own_diag_dist-opp_diag_dist)




def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic
    This measures the difference between the sum of the number of moves 
    available to a player within 3 spaces of a player and the sum of the
    number of moves available to their opponent

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #VERY BASIC HEURISTIC BASED ON THE SUM OF MOVES WITHIN 3 SPACES OF 
    # THE PLAYERS CURRENT LOCATION

    opponent = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    #diff_moves = float(own_moves - opp_moves)

    #Get the current location of each player
    p1_location = game.get_player_location(player)
    p2_location = game.get_player_location(opponent)

    # Return the number of legal moves which are in a proximity of 3 cells
    # to the opponent
    close_moves = 0
    for move in own_moves:
        if abs(move[0] - p2_location[0]) <= 3 and abs(move[1] - p2_location[1]) <= 3:
            close_moves += 1

    #print('close_moves : ', close_moves)
    return float(close_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic
    This measures the difference between the sum of the Manhattan distances 
    for each available move to a player relative to their opponents location
    and the sum of the Manhattan distances for each available move for an opponent
    relative to the players location


    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)


    p1_location = game.get_player_location(player)
    opp_location = game.get_player_location(opponent)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # WEIGHT VALUES BY THE DIFFERENCE IN THE SUM OF MANHATTAN VALUES
    # TAKEN FROM THE AVAILABLE MOVES, RELATIVE TO EACH PLAYERS CURRENT LOCATION
    own_weights = 0.0

    for move in own_moves:
        own_weights += math.sqrt((move[0]-opp_location[0])**2 + (move[1]-opp_location[1])**2)

    opp_weights = 0.0
    for move in opp_moves:
        opp_weights += math.sqrt((move[0]-p1_location[0])**2 + (move[1]-p1_location[1])**2)

    return float(own_weights - opp_weights)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            best_move = (-1,-1)
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves))-1]
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def min_value(game, depth):
            #Check the time
            time_check(self)
            moves = game.get_legal_moves()
            # No moves or at root, return the derived score
            if not moves or depth == 0:
                return self.score(game, self)
            # Set the upper bound for the score
            best_score = float('inf')
            for move in moves:
                # Forecast the next move
                score = max_value(game.forecast_move(move), depth-1)
                if score < best_score:
                    best_score = score
            return best_score

        def max_value(game, depth):
            # Check the time
            time_check(self)
            moves = game.get_legal_moves()
            # No moves or at root, return the derived score
            if not moves or depth == 0:
                return self.score(game, self)
            # Set the lower bound for the score
            best_score = float('-inf')
            #Iterate through available moves
            for move in moves:
                # Forecast gameplay from the move
                score = min_value(game.forecast_move(move), depth-1)
                if score > best_score:
                    best_score = score
            return best_score

        def MinimaxDecision(game, depth):
            '''
                Iterates through available moves and returns 
                the best choice for the move based on the scores
                forecasted by stepping through min_value and max_value
            '''
            time_check(self)
            player_moves = game.get_legal_moves()
            best_move = (-1,-1)
            if not player_moves or depth == 0:
                return best_move
            # Set the lower bound
            best_score = float('-inf')
            # iterate through the available moves, find the one with
            # the best potential for a win
            for move in player_moves:
                score = min_value(game.forecast_move(move), depth-1)            
                if score > best_score:
                    best_move = move
                    best_score = score 
            # Return the best value at depth == self.search_depth     
            return best_move

        if len(game.get_legal_moves()) == (game.width*game.height):
            best_move = (math.ceil(game.width/2), math.ceil(game.height/2))
        else:
            best_move = MinimaxDecision(game, depth)
        legal_moves = game.get_legal_moves()
        if best_move == (-1,-1) and len(legal_moves) > 0:
            best_move = legal_moves[random.randint(0, len(legal_moves))-1]
        return best_move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        #Implement the iterative deepening search
        '''
            TODO: The function seems to be going through
            the entire while loop until the last iteration before returning
        '''

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            best_move = (-1,-1)
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves))-1]
        depth = 0
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while time_left() > self.TIMER_THRESHOLD:
                depth += 1
                best_move = self.alphabeta(game, depth)   

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed
        
        return best_move

        

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizingPlayer=True):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def min_value(game, m_depth, alpha, beta):
            time_check(self)
            moves = game.get_legal_moves()
            best_move = (-1,-1)
            if not moves or m_depth == 0:
                return self.score(game, self), best_move
            # Set the upper bound
            best_score = float('inf')
            for move in moves:
                score, c_move = max_value(game.forecast_move(move), m_depth-1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                if best_score <= alpha:
                    return best_score, best_move
                # Update beta if needed
                beta = min(beta, best_score)
            return best_score, best_move

        def max_value(game, m_depth, alpha, beta):
            time_check(self)
            moves = game.get_legal_moves()
            best_move = (-1,-1)
            if not moves or m_depth == 0:
                return self.score(game, self), best_move
            # Set the lower bound
            best_score = float('-inf')
            for move in moves:
                score,c_move = min_value(game.forecast_move(move), m_depth-1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
                if best_score >= beta:
                    return best_score, best_move
                # Update alpha if needed
                alpha = max(alpha, best_score)
            return best_score, best_move

        def AlphaBetaSearch(game, depth, alpha, beta):
            '''
                Performs the first call to max_value, initializing
                the AlphaBeta tree pruning search. Set up slightly 
                different from Minimax in that at self.search_depth 
                it sends the call directly out rather than iterating
                through available moves. This required modifying the 
                min_value and max_value methods to return the score as
                well as the move, though the move found at self.search_depth
                is the one returned. 
            '''
            time_check(self)
            best_score, best_move = max_value(game, depth, alpha, beta)
            return best_move
        
        #If the game is unplayed, play the center move
        if len(game.get_legal_moves()) == (game.width*game.height):
            best_move = (math.ceil(game.width/2), math.ceil(game.height/2))
        else:
            # Perform AlphaBeta to determine the next best move
            best_move = AlphaBetaSearch(game, depth, alpha, beta)
        legal_moves = game.get_legal_moves()
        # If there is no best move, check to see if there are any legal
        # moves left to avoid a forfeit
        if best_move == (-1,-1) and len(legal_moves) > 0:
            best_move = legal_moves[random.randint(0, len(legal_moves))-1]
        return best_move
