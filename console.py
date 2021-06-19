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
        print(f'Dit ligt er op het bord: {board}')

    def rack_pretty_print(self, rack):
        colordict = {1: 'grey', 2: 'red', 3: 'yellow', 4: 'blue', 5: 'magenta'}
        black, red, yellow, cyan = [], [], [], []
        printstring = ''
        for i in sorted(rack):
            if i[0] < 5:
                printstring += ' ' + colored(i[1], colordict[i[0]])
            else:
                printstring += ' jokers: ' + colored(i[1], colordict[i[0]])
        print('Je hebt dit op je bord liggen:')
        print(printstring)
