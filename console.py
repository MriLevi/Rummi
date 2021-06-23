from termcolor import colored

class Console:

    def __init__(self):
        pass

    def text_gui(self, query, *answers):
        '''This function allows us to make a query with some answers and process the input'''
        while True:
            print(query)
            inp = input()
            answer = inp.lower() if inp.lower() in [str(answer) for answer in answers] else None
            if answer is not None:
                return answer
            else:
                print('Try again, that input was not valid')

    def board_pretty_print(self, board):
        '''This function prints the board in color in the terminal'''
        if len(board) == 0:
            pass
        else:
            printstring = ''
            for set in board:
                setstring = ''
                for tile in set:
                    setstring += f'{self.print_colored_tile(tile)}'
                printstring += f'[{setstring}] '
            print(printstring)

    def solution_pretty_print(self, solution):
        '''This function prints the solution in color in the terminal'''
        printstring = ''
        for set in solution['sets']:
            setstring = ''
            for tile in set:
                setstring += f'{self.print_colored_tile(tile)}'
            printstring += f'[{setstring}] '
        print(printstring)

    def print_colored_tile(self, tile):
        '''This function makes a colored string for a single tile '''
        colordict = {1: 'grey', 2: 'red', 3: 'yellow', 4: 'blue', 5: 'magenta'}
        return f'[{colored(tile[1], colordict[tile[0]])}]'

    def rack_pretty_print(self, rack):
        '''This function prints the rack in color in the terminal'''
        printstring = ''
        for i in sorted(rack):
            if i[0] < 5:
                printstring += ' ' + self.print_colored_tile(i)
            else:
                printstring += ' jokers: ' + self.print_colored_tile(i)
        print('These tiles are on your rack:')
        print(printstring)
