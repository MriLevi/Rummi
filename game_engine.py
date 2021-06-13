from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from collections import defaultdict
from console import Console


class RummikubGame:

    def __init__(self):
        self.board = defaultdict(list)
        self.winner = None
        self.sg = SetGenerator()
        self.solver = SolveTiles()
        self.bag = self.sg.generate_tiles()
        self.con = Console()

    def select_starting_player(self):
        '''This function determines a starting player by drawing 2 random tiles and comparing their values.'''
        starting_player_selected = False
        player_starts = None
        while not starting_player_selected:
            two_tiles = []
            for i in range(2):
                random_key = random.choices(list(self.bag.keys()), weights=[float(len(i)) for i in self.bag.values()],
                                            k=1)
                while self.bag[random_key[0]] == []:
                    random_key = random.choices(list(self.bag.keys()),
                                                weights=[float(len(i)) for i in self.bag.values()],
                                                k=1)
                random_value = random.choice(self.bag[random_key[0]])
                two_tiles.append(random_value)
            print(f'You drew {two_tiles[0]}, computer drew: {two_tiles[1]}')
            if two_tiles[0] > two_tiles[1]:
                print('You start!')
                starting_player_selected = True
                player_starts = True
            if two_tiles[1] > two_tiles[0]:
                print('Computer starts.')
                starting_player_selected = True
                player_starts = False
            elif two_tiles[0] == two_tiles[1]:
                print('Same values, drawing again...')
        return player_starts

    def draw_tile(self, rack=defaultdict(list), tile_amount=1):
        '''This function allows us to draw tiles.
           it takes rack as a parameter to append the drawn tiles to, and returns the updated rack.
           with the param tile_amount we can specify how many tiles to draw, and this allows us to use this function
           both for drawing single tiles and drawing starting racks.'''
        temprack = rack
        for i in range(1, tile_amount + 1):
            #select a random key based on how many tiles are still left in that colour
            #basically making sure we have equal chance of drawing any tile, as we select a random key first.
            #this method also means that we can't select empty keys, as they will have a weight of 0
            random_key = random.choices(list(self.bag.keys()), weights=[float(len(i)) for i in self.bag.values()], k=1)
            random_value = random.choice(self.bag[random_key[0]]) #chose a random tile within the chosen key
            temprack[random_key[0]].append(random_value) #append the chosen tile to the rack
            self.bag[random_key[0]].remove(random_value) #remove the tile from the bag
        return temprack

    def take_player_turn(self, board, rack):
        print('take player turn initialized')
        self.con.rack_pretty_print(rack)
        place_tiles = self.con.text_gui('Do you want to put tiles on the board?', 'yes', 'no')
        if place_tiles == 'yes':
            solutions = self.solver.solve_tiles(board, rack)
            self.con.text_gui('Which placement did you come up with?', solutions)
            return rack, board
        else:
            self.draw_tile(rack, tile_amount=1)
            return rack, board

    def take_computer_turn(self, board, rack):
        print('take computer turn initialized')
        print(f'rack:{rack}, board: {board}')
        if len(rack) == 0:
            self.winner = 'computer'
        #solutions = self.solver.solve_tiles(board, rack)
        return rack, board

