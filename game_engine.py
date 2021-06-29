from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from console import Console


class RummikubGame:

    def __init__(self):
        self.board = []
        self.winner = None
        self.sg = SetGenerator() #instantiate the set generator
        self.solver = SolveTiles() #instantiate the solver
        self.con = Console() #instantiate the console
        self.bag = self.sg.generate_tiles() #generate the tiles with the set generator


    def select_starting_player(self):
        '''This function determines a starting player by drawing 2 random tiles and comparing their values.'''
        starting_player_selected = False
        player_starts = None
        while not starting_player_selected: #as long as a starting player has not been determined
            two_tiles = []
            for i in range(2):
                random_tile = random.choice(self.bag) #draw a random tile
                while random_tile[0] == 5: #if we draw a joker, draw again
                    print('drew joker, drawing again...')
                    random_tile = random.choice(self.bag)
                two_tiles.append(random_tile)
            print(f'You drew {self.con.print_colored_tile(two_tiles[0])}, computer drew: {self.con.print_colored_tile(two_tiles[1])}')
            if two_tiles[0][1] > two_tiles[1][1]: #compare the values
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
        for i in range(1, tile_amount + 1): #draw tiles tile_amount times
            random_tile = random.choice(self.bag) #choose random tile
            temprack.append(random_tile) #append the chosen tile to the rack
            self.bag.remove(random_tile) #remove the tile from the bag
        return temprack #return the new rack after drawing tile

    def take_player_turn(self, board, rack):
        '''This is the function for a players turn. A player may choose to manually choose tiles (not implemented)
        or use the solver to solve their turn.'''
        print('Your turn! These tiles are on the table:')

        self.con.board_pretty_print(board) #print the board
        self.con.rack_pretty_print(rack)   #print the rack

        find_best_move = self.con.text_gui('Do you want to find the best move?', 'yes', 'no')
        if find_best_move == 'yes': #if player wants to use the solver
            solutions = self.solver.solve_tiles(board, rack)
            best_solution = self.find_best_solution(solutions)
            if best_solution == []:
                print('No move was possible, drawing a tile.')
                self.draw_tile(rack, tile_amount=1)
                return rack, board


            self.con.solution_pretty_print(best_solution)

            con_play = self.con.text_gui('Play the best solution?', 'yes', 'no')

            if con_play == 'yes':
                board = best_solution['sets']
                rack = best_solution['hand']
                return rack, board
            if con_play == 'no':
                self.draw_tile(rack, tile_amount=1)
                print('no play has been made, drawing a tile')
                return rack, board

        if find_best_move == 'no':
            what_play = self.con.text_gui('Which tiles do you want to play? (THIS IS NOT IMPLEMENTED, PLEASE USE SOLVER <3')
            #TODO: manual tile input

        else:
            self.draw_tile(rack, tile_amount=1)
            print('no play has been made, drawing tile')
            return rack, board

    def take_computer_turn(self, board, rack):
        '''This is the function for the computer's turn. It uses solve_tiels to find the best solution and plays it if able.
        If not able, it draws a tile and ends its turn.'''
        print('Computers turn')
        print('Computer is calculating best move...')
        if len(rack) == 0:
            self.winner = 'computer'

        solutions = self.solver.solve_tiles(board, rack)
        best_solution = self.find_best_solution(solutions)

        if best_solution == []:
            print('Computer could not make a move, draws a tile')
            self.draw_tile(rack, tile_amount=1)
            return rack, board

        else:
            board = best_solution['sets']
            rack = best_solution['hand']
            print('Computer plays tiles:')
            self.con.solution_pretty_print(best_solution)
            return rack, board

    def find_best_solution(self, solutions):
        '''This function checks the best solutions for validity by checking if the solution contains all board tiles'''
        score_solutions = [solution for solution in solutions if solution['score'] > 0] #make a new list of scoring solutions
        best_solution = [] #save the best solution here
        if self.board == []: #if there is nothing on the board
            try:
                best_solution = max(score_solutions, key=lambda x:x['score']) #filter solutions by score and find highest score
                return best_solution
            except: #exception only gets hit when solutions is empty
                return []
        else: #if we do have tiles on the board
            best_score = 0 #set best_score counter
            best_solution = [] #save best solution here
            flat_board = [tile for set in self.board for tile in set] #make a flat list of all tuples in board
            for solution in score_solutions: #for every solution in the filtered list
                #make a flat list with all tuples in solution that are same as board
                check_intersection = [tile for set in solution['sets'] for tile in set if tile in flat_board]
                #make a flat list that has all tiles of a solution
                flat_solution = [tile for set in solution['sets'] for tile in set]

                if len(check_intersection) == len(flat_solution): #if the solution has the same length as the intersection
                    continue #we dont add any new tiles with this solution, go to the next one
                elif len(check_intersection) < len(flat_board): #if the intersection has less tiles than the board
                    #then we are not using all board tiles, go to the next solution
                    continue
                else: #if all board tiles are used and we add new tiles with this solution:
                    if solution['score'] > best_score: #if it has a better score than our best_solution
                        best_score = solution['score'] #save the score
                        best_solution = solution #save the solution
            return best_solution #return the best solution


