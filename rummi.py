from game_engine import RummikubGame
from collections import defaultdict
from console import Console


def main():
    game = RummikubGame()
    con = Console()
    playerrack = defaultdict(list)
    playerrack = game.draw_tile(playerrack, tile_amount=14)
    computerrack = defaultdict(list)
    computerrack = game.draw_tile(computerrack, tile_amount=14)

    print('Welcome to Rummikub!')
    playerstarts = game.select_starting_player()

    while game.winner is None:
        if playerstarts:
            playerrack, game.board = game.take_player_turn(game.board, playerrack)
            computerrack, game.board = game.take_computer_turn(game.board, computerrack)
        else:
            computerrack, game.board = game.take_computer_turn(game.board, computerrack)
            playerrack, game.board = game.take_player_turn(game.board, playerrack)

    con.rack_pretty_print(playerrack)


main()
