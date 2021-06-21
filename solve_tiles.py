from set_generator import SetGenerator
import numpy as np
from itertools import combinations
from collections import defaultdict

class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']
        self.sg = SetGenerator()

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
        newsolutions = []
        if n>1:
            newsolutions.extend(solutions)
        print(f'at the start: {len(newsolutions)}')
        filtertiles = list(filter(lambda tile: (tile[1] == n), tiles))  #make a filtered list with only tiles from current value

        #here we call find_new_groups to find all the new possible groups at the current n value
        new_groups = self.find_new_groups(n, tiles)

        if len(new_groups) != 0: # if new groups are found
            newsolutions.extend(new_groups) #add all the new possible groups as a new solution to newsolutions

        #call start_new_runs to find all the new single tile solutions
        new_run_starts = self.start_new_runs(filtertiles, tiles)

        if len(new_run_starts) != 0: #if we can start new runs
            newsolutions.extend(new_run_starts) #add the newly started runs

        if n > 1: #only start looping over solutions if we've actually found solutions
            loop_solutions = solutions.copy()
            for solution in solutions:
                solutions_with_groups = self.find_new_groups(n, solution['hand'], solution)
                loop_solutions.extend(solutions_with_groups)
                newsolutions.extend(solutions_with_groups)
            for solution in loop_solutions:  # for every solution found so far
                solution_tiles = list(filter(lambda tile: (tile[1] == n or tile[0] == 5), solution['hand'])) #select only the n value tiles and jokers in hand
                for set in solution['sets']: #for every set in the current solution
                    # here we try to extend a run, if we do, we append the solution
                    if not self.isSetGroup(set): #if current set is not a group
                        for tile in solution_tiles: #for every tile in hand with current n value
                            if self.canExtend(tile, set): #check if the set can be extended
                                #extend it:
                                newset = set
                                newset.append(tile) #extend the set
                                tempsolution = defaultdict(list)  # create a new solution
                                tempsolution['sets'] = solution['sets'].copy()
                                tempsolution['sets'].remove(set)
                                tempsolution['sets'] += [newset] #append the new set to the solution
                                tempsolution['hand'] += self.copy_list_and_delete_tiles(tile, solution['hand']) #remove the used tile from hand
                                tempsolution['score'] = self.calculate_score(tempsolution['sets']) #calculate score
                                newsolutions.append(tempsolution) #append the new solution to list of solutions
                                break #if we've extended the current set, we can break out of this loop.



        #here we start to loop over existing solutions, to either extend runs or add new groups to them
        #TODO:
        #Extend all existing runs if possible
        #Check if extending and forming group is possible
        #If neither possible, discard the solution if the length of the run is 2 or lower
        #Checking jokers should happen here too. Extending a run is always possible with joker



        print(f'at the end: {len(newsolutions)}')
        for solution in newsolutions:
            print(solution['sets'])
        if n < 3:
            return self.test_solution_finder(n+1, newsolutions, tiles)
        else:
            return newsolutions
        #else:
            #return self.test_solution_finder(n+1, newsolutions, tiles)

    def find_new_groups(self, n, tiles, input_solution=None):
        '''this function finds all new groups, adds them to a new solution, and returns a list of solutions
        if any tiles are duplicate, we also add a solution in which we use the duplicate tiles in a new run'''
        tempsolutions = []
        filtertiles = list(filter(lambda tile: (tile[1] == n or tile[0] == 5), tiles)) # keep only the tiles with value equal to n

        # completely new solutions:
        # here we find groups at the current value, and append them to a new solution
        unique_tiles = list(set(filtertiles))  # new list with all unique tiles
        duplicate_tiles = list(set([i for i in filtertiles if filtertiles.count(i) > 1]))  # new list with all dupes

        if len(unique_tiles) > 2:  # groups have to be at least 3 tiles long
            for i in range(3, 5):  # for lengths 3 and 4
                for item in combinations(unique_tiles, i): # for every combination of tiles
                    tempitem = list(item)
                    solution = defaultdict(list)
                    # append the combination and strip the used tiles from remaining tiles
                    if item[0][0] == 5: #if we use a joker as the first tile
                        tempitem.insert(1, tempitem.pop(0)) #move it to the middle
                    if item[-1][0] == 5: #same for last tile
                        tempitem.insert(1, tempitem.pop(-1)) #move it to the middle
                    if tempitem [-1][0] == 5: #this means we are laying down 2 jokers in a group and it is not a legal move
                        continue              #and even if it was, its very bad strategy.

                    if input_solution is None: #if we are not working with an input solution:
                        solution['sets'] += [tempitem]
                        solution['hand'] += self.copy_list_and_delete_tiles(tempitem, tiles)
                    else:
                        solution['sets'] = input_solution['sets'].copy()
                        solution['sets'] += [tempitem]
                        solution['hand'] = self.copy_list_and_delete_tiles(tempitem, tiles)

                    solution['score'] = self.calculate_score(solution['sets'])
                    tempsolutions.append(solution)

                    #if we have duplicate tiles, also start a new run in the same solution with each of the duplicates
                    if len(duplicate_tiles) > 0:
                        for tile in duplicate_tiles:
                            dupe_solution = defaultdict(list)
                            newhand = self.copy_list_and_delete_tiles(tile, self.copy_list_and_delete_tiles(list(item), tiles))
                            if input_solution is None:
                                dupe_solution['sets'] += [list(item)]
                                dupe_solution['sets'] += [[tile]]
                            else:
                                dupe_solution['sets'] = input_solution['sets'].copy()
                                dupe_solution['sets'] += [list(item)]
                                dupe_solution['sets'] += [[tile]]

                            dupe_solution['hand'] = newhand
                            dupe_solution['score'] = self.calculate_score(dupe_solution['sets'])
                            tempsolutions.append(dupe_solution)
        return tempsolutions

    def calculate_score(self, hand):
        '''this function calculates the score for a given hand'''
        score = 0
        for set in hand:
            if len(set) > 2:
                for tile in set:
                    if tile[0] != 5:
                        score+= tile[1]
        return score

    def start_new_runs(self, tiles, hand):
        newsolutions = []
        for tile in tiles:
            # make a new solution with the current tile:
            tempsolution = defaultdict(list)
            tempsolution['sets'] += [[tile]]
            tempsolution['hand'] = self.copy_list_and_delete_tiles(tile, hand)
            tempsolution['score'] = self.calculate_score(tempsolution['sets'])
            newsolutions.append(tempsolution)
        return newsolutions

    def copy_list_and_delete_tiles(self, to_remove, tiles):
        if to_remove is None: #if nothing has to be removed, return the tiles
            return tiles
        else:
            templist = tiles.copy() #make a copy of the tiles
            if type(to_remove) is tuple: #if we remove just a single tile
                templist.remove(to_remove)
                return templist
            else: #if to_remove is a list of tiles to remove
                for tile in to_remove:
                    templist.remove(tile)
                return templist

    def canExtend(self, tile, set):
        if tile[0] == 5: #jokers can always extend a run
            return True
        if set[0][0] != tile[0]: #if the tile is not the same suit as the first tile of the set (which is never a joker)
            return False
        if set[-1][0] == 5: #if the last tile of the set is a joker
            if set[-2][1] == tile[1]-2: #if the tile before the joker has the same value as the tile, set is extendable
                return True
        if set[-1][1] == tile[1]-1: #if the value of the last tile in the set is one lower than the tile, set is extendable
            return True
        else:                       #set is not extendable
            return False

    def isSetGroup(self, set):
        if len(set) < 3: #groups are always at least 3 tiles long, so if its shorter, it's a run
            return False
        #Since we never use jokers at the outside of groups unless its a game winning move,
        #if the first and last tile of a set are of equal value, its a group.
        if set[0][1] == set[-1][1]:
            return True
        else:
            return False








