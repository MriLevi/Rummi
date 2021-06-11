from game_engine import RummikubGame
from collections import defaultdict
from console import Console


def sort_defaultdict(dict):
    for key, value in dict.items():
        newvalue = sorted(value)
        dict[key] = newvalue
    return dict

def main():
    game = RummikubGame()
    con = Console()
    playerrack = defaultdict(list)
    playerrack = sort_defaultdict(game.draw_tile(playerrack, tile_amount=14))
    computerrack = defaultdict(list)
    computerrack = sort_defaultdict(game.draw_tile(computerrack, tile_amount=14))

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
