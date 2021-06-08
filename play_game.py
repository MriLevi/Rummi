from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from collections import defaultdict
from players import Players

class RummikubGame:

    def __init__(self, players):
        self.players = players
        self.board = []
        self.winner = None
        sg = SetGenerator()
        self.bag = sg.generate_tiles()



    def generate_starting_rack(self):
        '''This function generates a random rack, based off items still left in bag'''
        rack = defaultdict(list)

        for i in range(1, 14):
            #we start by selecting a random key, based on how many values are in a given key
            #this makes sure we still actually draw at random. Instead of each key being 1 in 9 every time
            #we actually have equal odds on every single tile
            random_key = random.choices(list(self.bag.keys()), weights=[float(len(i)) for i in self.bag.values()], k=1)
            while self.bag[random_key[0]] == []:
                random_key = random.choice(list(self.bag.keys()))
            random_value = random.choice(self.bag[random_key[0]])
            rack[random_key[0]].append(random_value)
            self.bag[random_key[0]].remove(random_value)
        return rack

    def deal_tiles(self, bag, tile_count=14):
        for player in self.players:
            rack = self.generate_starting_rack(self.bag)
            player.rack = rack


def text_gui(query, *answers):
    while True:
        print(query)
        inp = input()
        answer = inp.lower() if inp.lower() in [str(answer) for answer in answers] else None
        if answer is not None:
            return answer
        else:
            print('Try again, that input was not valid')
def main():
    generate_players = Players()
    player1 = text_gui('What kind of player should player 1 be?', 'cpu', 'dumbcpu', 'human')
    players = None
    # if player1 == 'cpu':
    #     players += generate_players.dumb_bot()
    # elif player1 == 'dumbcpu':
    # elif player1 == 'human':
    # player2 = text_gui('What kind of player should player 2 be?', 'cpu', 'dumbcpu', 'human')
    # if player2 == 'cpu':
    # elif player2 == 'dumbcpu':
    # elif player2 == 'human':

main()
from set_generator import SetGenerator


