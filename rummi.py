from game_engine import RummikubGame
from console import Console

def main():
    '''This is the main gameplay loop'''
    #initialize needed classes
    game = RummikubGame()
    con = Console()
    playerrack = [] #create a new rack
    playerrack = game.draw_tile(playerrack, tile_amount=14) #draw 14 tiles to it
    computerrack = []
    computerrack = game.draw_tile(computerrack, tile_amount=14)

    print('Welcome to Rummikub!')
    playerstarts = game.select_starting_player() #select the starting player

    while game.winner is None: #gameplay loop
        if playerstarts:
            playerrack, game.board = game.take_player_turn(game.board, playerrack)
            computerrack, game.board = game.take_computer_turn(game.board, computerrack)
        else:
            computerrack, game.board = game.take_computer_turn(game.board, computerrack)
            playerrack, game.board = game.take_player_turn(game.board, playerrack)

main()
