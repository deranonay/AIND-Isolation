"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def get_open_moves(game, player):
    """
    :param game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells). 
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: tuple of player moves and inverted opponent moves normalised to 0-1 range.
    """
    max_move = 8
    player_moves = len(game.get_legal_moves(player)) / max_move
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player))) / max_move
    inv_opponent_moves = (float(1) / opponent_moves) if opponent_moves > 0 else float(1)
    return player_moves, opponent_moves


def get_distance_from_blanks(game, player):
    """
    :param game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells). 
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: inverted squared distance from centre of all blanks in the board
    """
    y, x = game.get_player_location(player)
    blanks = game.get_blank_spaces()
    sum_move = (0, 0)
    for blank in blanks:
        sum_move = (sum_move[0] + blank[0], sum_move[1] + blank[1])
    blanks_centre_y = float(sum_move[0] / len(blanks))
    blanks_centre_x = float(sum_move[1] / len(blanks))
    sq_dist_from_blanks = float((y - blanks_centre_y) ** 2 + (x - blanks_centre_x) ** 2)
    # sq_dist_from_blanks = (float(1) / sq_dist_from_blanks) if sq_dist_from_blanks > 0 else float(1)
    return sq_dist_from_blanks


def get_distance_to_centre(game, player):
    """
    :param game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells). 
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: inverted squared distance to the centre of the board
    """
    player_loc = game.get_player_location(player)
    centre_loc = game.width / 2, game.height / 2
    dist_to_centre = (player_loc[0] - centre_loc[0]) ** 2 + (player_loc[1] - centre_loc[1]) ** 2
    inv_dist_to_centre = (float(1) / dist_to_centre) if dist_to_centre > 0 else 1
    return dist_to_centre


def get_distance_to_opponent(game, player):
    """
    :param game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells). 
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: inverted squared distance to the opponent
    """
    player_loc = game.get_player_location(player)
    opponent_loc = game.get_player_location(game.get_opponent(player))
    dist_to_opp = (player_loc[0] - opponent_loc[0]) ** 2 + (player_loc[1] - opponent_loc[1]) ** 2
    inv_dist_to_opp = float(1) / dist_to_opp
    return dist_to_opp


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

    player_moves, opponent_moves = get_open_moves(game, player)
    return player_moves - opponent_moves


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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    sq_dist_from_blanks = get_distance_from_blanks(game, player)
    sq_dist_from_blanks_opp = get_distance_from_blanks(game, game.get_opponent(player))

    dist_to_opp = get_distance_to_opponent(game, player)
    dist_to_centre = get_distance_to_centre(game, player)

    return -sq_dist_from_blanks + sq_dist_from_blanks_opp - dist_to_centre - dist_to_opp


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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    dist_to_opp = get_distance_to_opponent(game, player)
    dist_to_centre = get_distance_to_centre(game, player)
    dist_from_blanks = get_distance_from_blanks(game, player)

    total_score = dist_to_centre + dist_from_blanks*2
    return float(1) / total_score if total_score > 0 else 1


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
    """
    Abstract IsolationPLayer class that defines some of the common functionality that is used by players that utilise 
    minimax search algorithm with or without alpha-beta pruning. Concrete classes extending this abstract class should 
    implement the search method with their choice of a search algorithm.
    """

    def search(self, game, depth):
        """
        :param game: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        :param depth: int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        :return: (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
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

            # Perform iterative deepening search.
            depth = 1
            while self.search_depth >= depth:
                best_move = self.search(game, depth)
                depth = depth + 1

        except SearchTimeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax_with_score(self, game, depth, alpha=float("-inf"), beta=float("inf"), apply_alphabeta=False):
        """
        :param game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        :param depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        :param alpha : float
            Alpha limits the lower bound of search on minimizing layers

        :param beta : float
            Beta limits the upper bound of search on maximizing layers
        :param apply_alphabeta: bool
            Flag that defines whether alpha beta pruning will be applied
        :return: 
        float
            Score corresponding to the best move found in the current search
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the score of the active player if bottom of the depth is reached or if there are no moves available
        legal_moves = game.get_legal_moves(game.active_player)
        maximising = game.active_player == self
        if depth == 0 or len(legal_moves) == 0:
            current_score = self.score(game, game.active_player if maximising else game.inactive_player)
            return current_score, None

        # Define helper functions that perform the right action depending on if the active player is a maximising player
        best_move = (float("-inf") if maximising else float("inf"), legal_moves[0])
        get_better_move = lambda x, y: max(x, y, key=lambda a: a[0]) if maximising else min(x, y, key=lambda a: a[0])
        updated_alpha = lambda a, x: max(a, x) if maximising else a
        updated_beta = lambda b, x: min(b, x) if not maximising else b

        # Pick the best move from available moves by iteratively calling minimax_with_score function
        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            (new_score, _) = self.minimax_with_score(forecasted_game, depth - 1, alpha, beta, apply_alphabeta)
            new_move = (new_score, move)
            best_move = get_better_move(new_move, best_move)

            # Apply alpha-beta pruning if the flag is set
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
