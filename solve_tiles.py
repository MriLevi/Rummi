from set_generator import SetGenerator
import numpy as np

class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']
        self.sg = SetGenerator()


    def sort_defaultdict(self, dict):
        for key, value in dict.items():
            newvalue=sorted(value)
            dict[key] = newvalue
        return dict

    def generate_matrix(self, tiles):
        matrix = np.zeros((self.sg.colors, self.sg.numbers))
        jokers = 0
        for tile in tiles:
            if tile[0] < 5: #if the tile is not a joker
                matrix[tile[0]-1][tile[1]-1] += 1 #up the value of tile in matrix
            else:
                jokers+=1
        return matrix, jokers

    #def max_score(self, value, runs):

    #def make_runs(self, tiles, jokers, rack):

        #return runs



    def solve_tiles(self, board=[], rack=[]):
        union = board+rack
        jokers = 0
        for tile in union:
            if tile[1] == 5:
                jokers+=1
        unionmatrix, jokers = self.generate_matrix(union)
        runs = np.zeros((self.sg.colors, self.sg.tile_sets))
        print(unionmatrix)
        for row in range(1, unionmatrix):
            for tile in range(1, row):
                if unionmatrix[row][tile] + unionmatrix[row][tile+1] == 2:
                    runs.append()
        #for runs, runscores in self.make_runs(unionmatrix):
        #runs = self.make_runs(union, jokers, rack)
        #return runs, rack, board







