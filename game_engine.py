from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
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
            print(f'You drew {self.con.print_colored_tile(two_tiles[0])}, computer drew: {self.con.print_colored_tile(two_tiles[1])}')
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
        print('Your turn! These tiles are on the table:')
        self.con.board_pretty_print(board)
        self.con.rack_pretty_print(rack)
        find_best_move = self.con.text_gui('Do you want to find the best move?', 'yes', 'no')
        if find_best_move == 'yes':
            solutions = self.solver.solve_tiles(board, rack)
            best_solution = max(solutions, key=lambda x:x['score'])

            if len(board) != 0:
                check_intersection = [x for x in best_solution['sets'] if x in board]
                if len(check_intersection) == len(board):
                    print('No solution is possible...')
                    self.draw_tile(rack, tile_amount=1)
                    print('Drawing a tile and ending turn.')
                    return rack, board


            if best_solution['score'] == 0:
                print('No solution is possible...')
                self.draw_tile(rack, tile_amount=1)
                print('Drawing a tile and ending turn.')
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
            what_play = self.con.text_gui('Which tiles do you want to play?')
            #TODO: manual tile input
        else:
            self.draw_tile(rack, tile_amount=1)
            print('no play has been made, drawing tile')
            return rack, board

    def take_computer_turn(self, board, rack):
        print('Computers turn')
        print('Computer is calculating best move...')
        if len(rack) == 0:
            self.winner = 'computer'

        solutions = self.solver.solve_tiles(board, rack)
        best_solution = max(solutions, key=lambda x: x['score'])

        if len(board) != 0:
            check_intersection = [x for x in best_solution['sets'] if x in board]
            if len(check_intersection) == len(board):
                print('Computer couldnt make a play')
                self.draw_tile(rack, tile_amount=1)
                print('Computer draws a tile and ends turn.')
                return rack, board
        if best_solution['score'] == 0:
            print('No solution is possible...')
            self.draw_tile(rack, tile_amount=1)
            print('Drawing a tile and ending turn.')
            return rack, board
        else:
            board = best_solution['sets']
            rack = best_solution['hand']
            print('Computer plays tiles:')
            self.con.solution_pretty_print(best_solution)
            return rack, board

        return rack, board

