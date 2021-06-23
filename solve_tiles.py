from set_generator import SetGenerator
from itertools import combinations
from collections import defaultdict
from console import Console

class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']
        self.sg = SetGenerator()
        self.con = Console()

    def solve_tiles(self, board=[], rack=[]):
        '''This function appends board and rack to each other and then calls solution_finder on the union'''
        union=[]
        for set in board:
            for tile in set:
                union.append(tile)
        union += rack
        solutions = self.solution_finder(1, [], union)
        return solutions

    def solution_finder(self, n=1, solutions=[], tiles=[]):
        '''This solution finder recursively finds every combination of tiles. It starts at n=1 which stands for tile value
            So first all tiles with value 1 are evaluated. at n=1, we start new runs and make new groups, and then make
            this function calls itsself with n+1 and all found solutions so far.
            At n=2, for example, we again find new runs and new groups, but we also try to find new groups/runs in existing solutions.
             We also try to extend runs in previous solutions. All these new solutions/options are saved and recursed on.'''
        newsolutions = []
        if n > 1:
            newsolutions.extend(solutions)

        # here we call find_new_groups to find all the new possible groups at the current n value
        new_groups = self.find_new_groups(n, tiles)

        if len(new_groups) != 0:  # if new groups are found
            newsolutions.extend(new_groups)  # add all the new possible groups as a new solution to newsolutions

        # call start_new_runs to find all the new single tile solutions
        new_run_starts = self.start_new_runs(tiles, n)

        if len(new_run_starts) != 0:  # if we can start new runs
            newsolutions.extend(new_run_starts)  # add the newly started runs

        if n > 1:  # only start looping over solutions if we've actually found solutions

            #first we populate the solutions to loop over by first adding groups
            #so we can loop over any leftover tiles
            loop_solutions = solutions.copy()
            for solution in solutions:
                # for every solution, add groups if possible
                solutions_with_groups = self.find_new_groups(n, solution['hand'], solution)
                loop_solutions.extend(solutions_with_groups)  # add the new solutions to loop_solutions
                newsolutions.extend(solutions_with_groups)  # add to the final solutions

                # for every solution, start new runs in them as well
                solutions_with_new_runs = self.start_new_runs(solution['hand'], n, solution)
                loop_solutions.extend(solutions_with_new_runs)
                newsolutions.extend(solutions_with_new_runs)
            for solution in loop_solutions:  # for every solution found so far
                newsolutions.extend(self.extend_runs(solution, n))  # extend the runs, add them to newsolutions

        if n < 14:
            return self.solution_finder(n + 1, newsolutions, tiles)
        else:
            return newsolutions

    def find_new_groups(self, n, tiles, input_solution=None):
        '''this function finds all new groups, adds them to a new solution, and returns a list of solutions
        if any tiles are duplicate, we also add a solution in which we use the duplicate tiles in a new run'''
        tempsolutions = []

        filtertiles = list(filter(lambda tile: (tile[1] == n or tile[0] == 5), tiles))  # keep only the tiles with value equal to n
        if len(filtertiles) > 2:
            # here we find groups at the current value, and append them to a new solution
            unique_tiles = list(set(filtertiles))  # new list with all unique tiles
        else:
            return []
        if len(filtertiles) > len(unique_tiles):
            duplicate_tiles = list(set([i for i in filtertiles if filtertiles.count(i) > 1]))  # new list with all dupes
            duplicates = True
        else:
            duplicates = False
        if len(unique_tiles) > 2:  # groups have to be at least 3 tiles long, if we don't have more than 2 unique tiles, no groups are possible
            for i in range(3, 5):  # for lengths 3 and 4
                for item in combinations(unique_tiles, i):  # for every combination of tiles
                    tempitem = list(item) #covert the item to a list temporarily
                    solution = defaultdict(list) #make a new solution
                    # append the combination and strip the used tiles from remaining tiles

                    if item[0][0] == 5:  # if we use a joker as the first tile
                        tempitem.insert(1, tempitem.pop(0))  # move it to the middle
                    if item[-1][0] == 5:  # same for last tile
                        tempitem.insert(1, tempitem.pop(-1))  # move it to the middle
                    if tempitem[-1][0] == 5:  #this means we are laying down 2 jokers in a group and it is not a legal move
                        continue              #and even if it was, its very bad strategy.

                    if input_solution is None:  # if we are not working with an input solution:
                        solution['sets'] += [tempitem]
                        solution['hand'] += self.copy_list_and_delete_tiles(tempitem, tiles)
                    else:
                        solution['sets'] = input_solution['sets'].copy()
                        solution['sets'] += [tempitem]
                        solution['hand'] = self.copy_list_and_delete_tiles(tempitem, tiles)
                    solution['score'] = self.calculate_score(solution['sets'])
                    tempsolutions.append(solution)

                    # if we have duplicate tiles, also start a new run in the same solution with each of the duplicates
                    if duplicates:
                        for tile in duplicate_tiles:
                            dupe_solution = defaultdict(list)
                            newhand = self.copy_list_and_delete_tiles(tile, self.copy_list_and_delete_tiles(list(item),                                                                          tiles))
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

    def extend_runs(self, solution, n):
        '''In this function we try to extend runs for a given solution and a given n value.'''
        extended_run_solutions = []
        solution_tiles = list(filter(lambda tile: (tile[1] == n or tile[0] == 5),
                                     solution['hand']))  # select only the n value tiles and jokers in hand
        if len(solution_tiles) > 0:  # if we have any tiles leftover
            for tile_set in solution['sets']:  # for every set in the current solution
                tempsolution = defaultdict(list)  # create a new solution
                tempsolution['sets'] = solution['sets'].copy()
                # here we try to extend a run, if we do, we append the solution
                if not self.is_set_group(tile_set):  # if current set is not a group
                    for tile in solution_tiles:  # for every tile in hand with current n value
                        if self.can_extend(tile, tile_set):  # check if the set can be extended
                            # extend it:
                            newset = tile_set.copy()
                            newset.append(tile)  # extend the set
                            solution_tiles.remove(tile)  # remove the tile
                            tempsolution['sets'].remove(tile_set)
                            tempsolution['sets'] += [newset]  # append the new set to the solution
                            tempsolution['hand'] = self.copy_list_and_delete_tiles(tile, solution[
                                'hand'])  # remove the used tile from hand
                            tempsolution['score'] = self.calculate_score(tempsolution['sets'])  # calculate score
                            extended_run_solutions.append(tempsolution)  # append the new solution to list of solutions
                            break  # if we've extended a set, no need to check other tiles
                else:
                    continue
            tempsolution['score'] = self.calculate_score(tempsolution['sets'])  # calculate score
            if tempsolution['score'] != 0:
                extended_run_solutions.append(tempsolution)  # append the new solution to list of solutions
        return extended_run_solutions

    def start_new_runs(self, tiles, n, input_solution=None):
        '''In this function we start new runs.'''
        new_runs = []
        filtertiles = list(filter(lambda tile: (tile[1] == n or tile[0] == 5), tiles)) #select only tiles of value n, or jokers

        for i in range(1, len(filtertiles)+1): #for length of combinations from 1 to length of the filtertiles:
            for item in combinations(filtertiles, i): #find every combination with length i
                tempsolution = defaultdict(list) #make a new solution
                tempitem = list(item) #convert the combination to a list
                if input_solution == None: #if there's no inputted solution
                    if len(item) == 1: #if there's only one tile
                        set_to_append = [tempitem]
                    else:
                        set_to_append = []
                        for j in range(0, len(tempitem)):
                            set_to_append.append([tempitem[j]]) #we need to do this to keep correct formatting

                    tempsolution['sets'] += set_to_append
                    tempsolution['hand'] = self.copy_list_and_delete_tiles(set_to_append, tiles)
                    tempsolution['score'] = self.calculate_score(tempsolution['sets'])
                    new_runs.append(tempsolution) #append the found solution
                else: #if there is an input solution
                    tempsolution['sets'] = input_solution['sets'].copy() #copy the sets in the solution into the new solution-set
                    if len(item) == 1:
                        set_to_append = [tempitem]
                    else:
                        set_to_append = []
                        for j in range(0, len(tempitem)):
                            set_to_append.append([tempitem[j]])
                    tempsolution['sets'] += set_to_append
                    tempsolution['hand'] = self.copy_list_and_delete_tiles(set_to_append, input_solution['hand'])
                    tempsolution['score'] = self.calculate_score(tempsolution['sets'])
                    new_runs.append(tempsolution)
        return new_runs

    @staticmethod
    def can_extend(tile, set):
        '''This function returns true if the inputted tile can extend the inputted set, otherwise returns false'''
        if tile[0] == 5 and set[-1][0] == 5: #jokers can always extend other jokers
            return True
        if tile[0] == 5 and set[-1][1] < 13: # jokers can always extend a run, but cannot be used as 14's, as they dont exist
            return True
        if len(set) == 1 and set[0][0] == 5 and tile[1] > 1: #if a run exists with only a joker in it, extendable if tile > 1
            return True
        elif set[0][0] != tile[0]:  # if the tile is not the same suit as the first tile of the set (which is never a joker)
            return False
        elif set[-1][1] == tile[1] - 1:  # if the value of the last tile in the set is one lower than the tile, set is extendable
            return True
        elif set[-1][0] == 5:  # if the last tile of the set is a joker
            if set[-2][0] == 5: # if the tile before that is also a jjoker
                if len(set) > 2:
                    if set[-3][1] == tile[1]-3:
                        return True
            elif set[-2][1] == tile[1] - 2:  # if the tile before the joker has the same value as the tile-2, set is extendable
                return True

        else:  # set is not extendable
            return False

    @staticmethod
    def is_set_group(set):
        '''This function returns true if the given set is a group, otherwise returns false'''
        if len(set) < 3:  # groups are always at least 3 tiles long, so if its shorter, it's a run
            return False
        # Since we never use jokers at the outside of groups unless its a game winning move,
        # if the first and last tile of a set are of equal value, its a group.
        if set[0][1] == set[-1][1]:
            return True
        else:
            return False

    @staticmethod
    def calculate_score(hand):
        '''this function calculates the score for a given hand'''
        score = 0
        for set in hand:
            if len(set) > 2:
                for tile in set:
                    if tile[0] != 5: #jokers do not award points
                        score += tile[1] #score is the value of all tiles combined
            else:  # if any set is not longer than two, solution awards no score
                score = 0
                return score
        return score

    @staticmethod
    def copy_list_and_delete_tiles(to_remove, tiles):
        '''This function takes to_remove as input and removes the contents from tiles
            Mostly used to strip used tiles from hand.'''
        if to_remove is None:  # if nothing has to be removed, return the tiles
            return tiles
        else:
            templist = tiles.copy()  # make a copy of the tiles
            if type(to_remove) is tuple:  # if we remove just a single tile
                templist.remove(to_remove)
                return templist
            else:  # if to_remove is a list of tiles to remove
                for tile in to_remove:
                    if type(tile) is tuple:
                        templist.remove(tile)
                    else:
                        for tupletile in tile:
                            templist.remove(tupletile)
                return templist
