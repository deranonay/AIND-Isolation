"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

NUM_MATCHES = 10  # number of matches against each opponent
TIME_LIMIT = 20  # number of milliseconds before timeout (orig=150)
MAX_DEPTH = 50

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation function
against the `ID_Improved` agent baseline. `ID_CustomScore` is an agent using
Iterative Deepening and the custom_score function defined in game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    last_lost_game_moves = []
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        count = 0
        for game in games:
            winner, move_hist, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1
            if winner.name != "AB_Custom" and game.active_player.name == "AB_Custom":
                last_lost_game_moves.append(("P1" if game.move_count % 2 else "P2", move_hist))
            count += 1

        if termination == "timeout":
            timeout_count += 1
        elif winner not in test_agents and termination == "forfeit":
            forfeit_count += 1

    return timeout_count, forfeit_count, last_lost_game_moves


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches):
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)

    print("\n{:^9}{:^13}{:^13}{:^13}{:^13}{:^13}".format(
        "Match #", "Opponent", test_agents[0].name, test_agents[1].name,
        test_agents[2].name, test_agents[3].name))
    print("{:^9}{:^13} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5}"
          .format("", "", *(["Won", "Lost"] * 4)))

    for idx, agent in enumerate(cpu_agents):
        wins = {test_agents[0].player: 0,
                test_agents[1].player: 0,
                test_agents[2].player: 0,
                test_agents[3].player: 0,
                agent.player: 0}

        print("{!s:^9}{:^13}".format(idx + 1, agent.name), end="", flush=True)

        timeout_count, forfeit_count, move_hist = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += timeout_count
        total_forfeits += forfeit_count
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        print(" {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5}"
              .format(*round_totals))
        for hist in move_hist:
            print("\t\t\t\t{} {}".format(hist[0], hist[1]))

    print("-" * 74)
    print("{:^9}{:^13}{:^13}{:^13}{:^13}{:^13}\n".format(
        "", "Win Rate:",
        *["{:.1f}%".format(100 * total_wins[a.player] / total_matches)
          for a in test_agents]
    ))

    if total_timeouts:
        print(("\nThere were {} timeouts during the tournament -- make sure " +
               "your agent handles search timeout correctly, and consider " +
               "increasing the timeout margin for your agent.\n").format(
            total_timeouts))
    if total_forfeits:
        print(("\nYour ID search forfeited {} games while there were still " +
               "legal moves available to play.\n").format(total_forfeits))


def main():
    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        Agent(AlphaBetaPlayer(search_depth=1, score_fn=improved_score), "AB_Improved"),
        Agent(AlphaBetaPlayer(search_depth=MAX_DEPTH, score_fn=custom_score, name="AB_Custom"), "AB_Custom"),
        Agent(AlphaBetaPlayer(search_depth=1, score_fn=custom_score_2), "AB_Custom_2"),
        Agent(AlphaBetaPlayer(search_depth=1, score_fn=custom_score_3), "AB_Custom_3")
    ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(), "Random"),
        Agent(MinimaxPlayer(search_depth=MAX_DEPTH, score_fn=open_move_score), "MM_Open"),
        Agent(MinimaxPlayer(search_depth=MAX_DEPTH, score_fn=center_score), "MM_Center"),
        Agent(MinimaxPlayer(search_depth=MAX_DEPTH, score_fn=improved_score), "MM_Improved"),
        Agent(AlphaBetaPlayer(search_depth=MAX_DEPTH, score_fn=open_move_score), "AB_Open"),
        Agent(AlphaBetaPlayer(search_depth=MAX_DEPTH, score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(search_depth=MAX_DEPTH, score_fn=improved_score), "AB_Improved")
    ]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))
    play_matches(cpu_agents, test_agents, NUM_MATCHES)


if __name__ == "__main__":
    main()
