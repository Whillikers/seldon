"""
Wrapper code to make players compatible with Caltech's CS2 framework.
A player should be configured with a "player config" file, which
can be called as a script or embedded into C with `cython --embed`.
"""

import logging
import sys
from typing import Optional, Type

from board import Board, Loc, PlayerColor
from player import PlayerABC


def run_player(player_class: Type[PlayerABC], **player_kwargs) -> None:
    player: Optional[PlayerABC] = None
    color = {"Black": PlayerColor.BLACK, "White": PlayerColor.WHITE}[sys.argv[1]]
    board = Board.starting_board()
    print(f"Player ready: {player_class.__name__} ({color.value})")

    while True:
        opp_x_, opp_y_, ms_left_ = input().split()
        opp_x, opp_y, ms_left = int(opp_x_), int(opp_y_), int(ms_left_)

        if player is None:
            ms_tot = ms_left if ms_left > 0 else None
            player = player_class(color, ms_tot, **player_kwargs)  # type: ignore
            player.logger.setLevel(logging.DEBUG)

        if opp_x < 0:  # Opponent passed
            last_move = None
        else:
            last_move = Loc(opp_x, opp_y)
            board = board.resolve_move(last_move, color.opponent)

        move = player.get_move(board, last_move, ms_left)
        if move != Loc.pass_loc():
            board = board.resolve_move(move, color)
        print(f"{move.x} {move.y}")