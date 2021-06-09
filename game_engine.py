from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from collections import defaultdict

class RummikubGame:

    def __init__(self):
        self.board = []
        self.winner = None
        sg = SetGenerator()
        self.bag = sg.generate_tiles()

    def draw_tile(self, rack=defaultdict(list), tile_amount=1):
        temprack = rack
        for i in range(1, tile_amount+1):
            random_key = random.choices(list(self.bag.keys()), weights=[float(len(i)) for i in self.bag.values()], k=1)
            while self.bag[random_key[0]] == []:
                random_key = random.choices(list(self.bag.keys()), weights=[float(len(i)) for i in self.bag.values()], k=1)
            random_value = random.choice(self.bag[random_key[0]])
            temprack[random_key[0]].append(random_value)
            self.bag[random_key[0]].remove(random_value)
        return temprack




    #def take_turn(self):

