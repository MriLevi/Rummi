from termcolor import colored

class Console:

    def __init__(self):
        pass

    def text_gui(self, query, *answers):
        while True:
            print(query)
            inp = input()
            answer = inp.lower() if inp.lower() in [str(answer) for answer in answers] else None
            if answer is not None:
                return answer
            else:
                print('Try again, that input was not valid')

    def board_pretty_print(self, board):
        if len(board) == 0:
            pass
        else:
            print(f'These tiles are on the table: {board}')

    def print_colored_tile(self, tile):
        colordict = {1: 'grey', 2: 'red', 3: 'yellow', 4: 'blue', 5: 'magenta'}
        return f'[{colored(tile[1], colordict[tile[0]])}]'
    def rack_pretty_print(self, rack):
        black, red, yellow, cyan = [], [], [], []
        printstring = ''
        for i in sorted(rack):
            if i[0] < 5:
                printstring += ' ' + self.print_colored_tile(i)
            else:
                printstring += ' jokers: ' + self.print_colored_tile(i)
        print('These tiles are on your rack:')
        print(printstring)
