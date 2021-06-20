from set_generator import SetGenerator
import numpy as np
from itertools import combinations

class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']
        self.sg = SetGenerator()

    # def generate_matrix(self, tiles):
    #     matrix = np.zeros((self.sg.colors, self.sg.numbers))
    #     jokers = 0
    #     for tile in tiles:
    #         if tile[0] < 5: #if the tile is not a joker
    #             matrix[tile[0]-1][tile[1]-1] += 1 #up the value of tile in matrix
    #         else:
    #             jokers+=1
    #     return matrix, jokers

    def solve_tiles(self, board=[], rack=[]):
        boardjokers = 0
        for i in board:
            if i[0] == 5:
                boardjokers+=1
        union = board+rack
        jokers = 0
        #boardmatrix, boardjokers = self.generate_matrix(board)
        #unionmatrix, jokers = self.generate_matrix(union)
        solutions = self.test_solution_finder(1, [], union)

    def test_solution_finder(self, n=1, solutions=[], tiles=[]):
        print(f'current n: {n}')
        newsolutions = solutions.copy() #save all the found solutions
        filtertiles = list(filter(lambda tile: (tile[1] == n), tiles))  #make a filtered list with only tiles from current value

        #here we call find_new_groups to find all the new possible groups at the current n value
        new_groups = self.find_new_groups(n, tiles)
        newsolutions.extend(new_groups) #add all the new possible groups as a new solution to newsolutions



        #here we make new solutions where we simply add the current tile to a new solution, to possibly make new runs later
        for tile in filtertiles:
            # make a new solution with the current tile:
            newsolutions.append([[tile], self.copy_list_and_delete_tiles(tile, tiles)])

        #here we start to loop over existing solutions, to either extend runs or add new groups to them
        #TODO:
        #Extend all existing runs if possible
        #Check if extending and forming group is possible
        #If neither possible, discard the solution if the length of the run is 2 or lower
        #Checking jokers should happen here too. Extending a run is always possible with joker

        if n>1:
            for solution in solutions:
                print(f'solution: {solution}')
                #filtertiles = list(filter(lambda tile: (tile[1] == n), remaining_tiles))  # keep only the tiles with value equal to n

        print(f'amount of new solutions: {len(newsolutions)}')
        for solution in newsolutions:
            print(f'{solution}')

        if n < 14:
            return self.test_solution_finder(n+1, newsolutions, tiles)
        else:
            return newsolutions
        #else:
            #return self.test_solution_finder(n+1, newsolutions, tiles)

    def find_new_groups(self, n, tiles):
        '''this function finds all new groups, adds them to a new solution, and returns a list of solutions
        if any tiles are duplicate, we also add a solution in which we use the duplicate tiles in a new run'''
        tempsolutions = []
        filtertiles = list(filter(lambda tile: (tile[1] == n), tiles))  # keep only the tiles with value equal to n

        # completely new solutions:
        # here we find groups at the current value, and append them to a new solution
        unique_tiles = list(set(filtertiles))  # new list with all unique tiles
        duplicate_tiles = list(set([i for i in filtertiles if filtertiles.count(i) > 1]))  # new list with all dupes

        if len(unique_tiles) > 2:  # groups have to be at least 3 tiles long
            for i in range(3, 5):  # for lengths 3 and 4
                for item in combinations(unique_tiles, i):  # for every combination of tiles
                    # append the combination and strip the used tiles from remaining tiles
                    tempsolutions.append([[list(item)], self.copy_list_and_delete_tiles(list(item), tiles)])
                    # if we have duplicate tiles, also start a new run in the same solution with each of the duplicates
                    if len(duplicate_tiles) > 0:
                        for tile in duplicate_tiles:
                            newhand = self.copy_list_and_delete_tiles(tile, self.copy_list_and_delete_tiles(list(item), tiles))
                            print(f'tiles: {tiles}, {tile, item} newhand {newhand}')
                            tempsolutions.append([item, tile, self.copy_list_and_delete_tiles(newhand, tiles)])
        return [tempsolutions]



    def copy_list_and_delete_tiles(self, to_remove, tiles):
        #print(f'list: {to_remove}, tiles: {tiles}')
        if to_remove is None:
            return tiles
        else:
            templist = tiles.copy()
            if type(to_remove) is tuple:
                templist.remove(to_remove)
                return templist
            else:
                for tile in to_remove:
                    #print(f'tile: {tile}, templist: {templist}')
                    templist.remove(tile)
                return templist









