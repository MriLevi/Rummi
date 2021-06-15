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
        black, yellow, red, cyan, jokers = [], [], [], [], []
        for key, value in rack.items():

            if 'black' in key:
                if len(value) == 1:
                    black.append(value[0])
                else:
                    for i in value:
                        black.append(i)
            if 'yellow' in key:
                if len(value) == 1:
                    yellow.append(value[0])
                else:
                    for i in value:
                        yellow.append(i)
            if 'red' in key:
                if len(value) == 1:
                    red.append(value[0])
                else:
                    for i in value:
                        red.append(i)
            if 'cyan' in key:
                if len(value) == 1:
                    cyan.append(value[0])
                else:
                    for i in value:
                        cyan.append(i)
            if 'jokers' in key:
                if len(value) == 1:
                    jokers.append(value[0])
                else:
                    for i in value:
                        jokers.append(i)
        print(
            f'Je hebt dit op je bord:\n Zwart: {sorted(black)}, Geel: {sorted(yellow)}, Rood: {sorted(red)}, Cyaan: {sorted(cyan)}, jokers: {sorted(jokers)}')