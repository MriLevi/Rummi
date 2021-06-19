from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from collections import defaultdict
from console import Console


class RummikubGame:

    def __init__(self):
        self.board = []
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
                random_tile = random.choice(self.bag)
                while random_tile[0] == 5:
                    print('drew joker, drawing again...')
                    random_tile = random.choice(self.bag)
                two_tiles.append(random_tile)
            print(two_tiles)
            print(f'You drew {two_tiles[0]}, computer drew: {two_tiles[1]}')
            if two_tiles[0][1] > two_tiles[1][1]:
                print('You start!')
                starting_player_selected = True
                player_starts = True
            if two_tiles[0][1] < two_tiles[1][1]:
                print('Computer starts.')
                starting_player_selected = True
                player_starts = False
            elif two_tiles[0][1] == two_tiles[1][1]:
                print('Same values, drawing again...')
        return player_starts

    def draw_tile(self, rack=[], tile_amount=1):
        '''This function allows us to draw tiles.
           it takes rack as a parameter to append the drawn tiles to, and returns the updated rack.
           with the param tile_amount we can specify how many tiles to draw, and this allows us to use this function
           both for drawing single tiles and drawing starting racks.'''
        temprack = rack
        for i in range(1, tile_amount + 1):
            #select a random key based on how many tiles are still left in that colour
            #basically making sure we have equal chance of drawing any tile, as we select a random key first.
            #this method also means that we can't select empty keys, as they will have a weight of 0
            random_tile = random.choice(self.bag)
            temprack.append(random_tile) #append the chosen tile to the rack
            self.bag.remove(random_tile) #remove the tile from the bag
        return temprack

    def take_player_turn(self, board, rack):
        print('take player turn initialized')
        self.con.board_pretty_print(board)
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
        if len(rack) == 0:
            self.winner = 'computer'
        #solutions = self.solver.solve_tiles(board, rack)
        return rack, board

