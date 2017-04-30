"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    w, h = game.width, game.height
    y, x = game.get_player_location(player)
    sq_dist = float((h - y) ** 2 + (w - x) ** 2)

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(player_moves - opponent_moves**2)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    player_moves = len(game.get_legal_moves(player))
    return float(player_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(-opponent_moves)


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
    def __init__(self, search_depth=999, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxBasedIsolationPlayer(IsolationPlayer):

    def search(self, game, depth):
        raise NotImplementedError

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
        try:
            # Return immediately if there are no legal moves
            legal_moves = game.get_legal_moves(game.active_player)
            if len(legal_moves) == 0:
                return -1, -1

            # Default to a random legal move until we find a better one (in case timeout happens too quick)
            best_move = legal_moves[0]

            depth = 1
            while self.search_depth >= depth:
                best_move = self.search(game, depth)
                depth = depth + 1

        except SearchTimeout:
            # Handle any actions required at timeout, if necessary
            # print('Timed out at depth {}'.format(depth))
            return best_move

        # Return the best move from the last completed search iteration
        # raise NotImplementedError
        # print('Final selected move is {}'.format(best_move))
        return best_move

    def minimax_with_score(self, game, depth, alpha=float("-inf"), beta=float("inf"),
                           apply_alphabeta=False):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        is_maximising_player = game.active_player == self
        legal_moves = game.get_legal_moves(game.active_player)
        if depth == 0 or len(legal_moves) == 0:
            current_score = self.score(game, game.active_player if is_maximising_player else game.inactive_player)
            # print('score is {}'.format(current_score))
            return current_score, legal_moves[0] if len(legal_moves) > 0 else (-1, -1)

        best_move = (float("-inf") if is_maximising_player else float("inf"), legal_moves[0])
        get_better_move = lambda x, y: max(x, y, key=lambda a: a[0]) if is_maximising_player else min(x, y,
                                                                                                      key=lambda a: a[
                                                                                                          0])
        updated_alpha = lambda a, x: max(a, x) if is_maximising_player else a
        updated_beta = lambda b, x: min(b, x) if not is_maximising_player else b

        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            (new_score, _) = self.minimax_with_score(forecasted_game, depth - 1, alpha, beta, apply_alphabeta)
            new_move = (new_score, move)
            best_move = get_better_move(new_move, best_move)
            if apply_alphabeta:
                alpha = updated_alpha(alpha, best_move[0])
                beta = updated_beta(beta, best_move[0])
                if alpha >= beta:
                    break

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
        return self.minimax_with_score(game, depth)[1]

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
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
        return self.minimax_with_score(game, depth, alpha, beta, True)[1]


class MinimaxPlayer(MinimaxBasedIsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def search(self, game, depth):
        return self.minimax(game, depth)


class AlphaBetaPlayer(MinimaxBasedIsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def search(self, game, depth):
        return self.alphabeta(game, depth)
