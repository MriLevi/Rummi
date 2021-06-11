from game_engine import RummikubGame
import set_generator
import solve_tiles
from collections import defaultdict


def text_gui(query, *answers):
    while True:
        print(query)
        inp = input()
        answer = inp.lower() if inp.lower() in [str(answer) for answer in answers] else None
        if answer is not None:
            return answer
        else:
            print('Try again, that input was not valid')


def rack_pretty_print(rack):
    black, yellow, red, cyan, jokers = [], [], [], [], []
    for key, value in rack.items():

        if 'black' in key:
            if len(value) == 1:
                black.append(value[0])
            else:
                for i in value:
                    black.append(i)
        if 'yellow' in key:
            if len(value) == 1:
                yellow.append(value[0])
            else:
                for i in value:
                    yellow.append(i)
        if 'red' in key:
            if len(value) == 1:
                red.append(value[0])
            else:
                for i in value:
                    red.append(i)
        if 'cyan' in key:
            if len(value) == 1:
                cyan.append(value[0])
            else:
                for i in value:
                    cyan.append(i)
        if 'jokers' in key:
            if len(value) == 1:
                jokers.append(value[0])
            else:
                for i in value:
                    jokers.append(i)
    print(
        f'Je hebt dit op je bord:\n Zwart: {sorted(black)}, Geel: {sorted(yellow)}, Rood: {sorted(red)}, Cyaan: {sorted(cyan)}, jokers: {sorted(jokers)}')


def main():
    game = RummikubGame()
    playerrack = defaultdict(list)
    playerrack = game.draw_tile(playerrack, tile_amount=14)
    computerrack = defaultdict(list)
    computerrack = game.draw_tile(computerrack, tile_amount=14)
    playerfirsttile = next(iter(playerrack))
    computerfirsttile = next(iter(computerrack))
    playerstarts = True

    print('Welkom bij rummikub!')
    print(f'De computers eerste tegel is:{computerrack[computerfirsttile][0]}')
    print(f'Jouw eerste tegel is: {playerrack[playerfirsttile][0]}')

    if computerrack[computerfirsttile][0] > playerrack[playerfirsttile][0]:
        print('De computer begint!')
        playerstarts = False
    else:
        print('Jij begint!')
    while game.winner is None:
        if playerstarts:
            playerrack, game.board = game.take_player_turn()
            computerrack, game.board = game.take_computer_turn()
        else:
            computerrack, game.board = game.take_computer_turn()
            playerrack, game.board = game.take_player_turn()

    rack_pretty_print(playerrack)


main()
