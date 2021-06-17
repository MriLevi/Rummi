import itertools
from set_generator import SetGenerator
from collections import defaultdict


class SolveTiles:

    def __init__(self):
        self.yellow = ['yellow_1', 'yellow_2']
        self.cyan = ['cyan_1', 'cyan_2']
        self.black = ['black_1', 'black_2']
        self.red = ['red_1', 'red_2']


    def sort_defaultdict(self, dict):
        for key, value in dict.items():
            newvalue=sorted(value)
            dict[key] = newvalue
        return dict

    def solve_tiles(self, board, rack):
        sg = SetGenerator()
        runs = defaultdict(list)  # generate a default dict with lists as values
        sorted_rack = self.sort_defaultdict(rack)
        print(f'sorted rack: {sorted_rack}')
        runs = sg.generate_valid_runs(rack)
        groups = sg.generate_valid_groups(rack)
        sets = sg.generate_possible_sets(runs, groups)
        print(f'found runs: {runs}')
        print(f'found groups: {groups}')
        print(f'found sets: {sets}')
        pointsdict = self.points(sets)
        best_play = self.find_best_play(rack, pointsdict)
        return runs, rack, board

    def points(self, possiblesolution):
        pointsdict = defaultdict(list)
        for run in possiblesolution['runs']:
            for key in run.keys():
                for list_of_values in run[key]:
                    runpoints = 0
                    tempvalue = []
                    tempvalue.append(list_of_values)
                    for value in list_of_values:
                        if value != 'j1' and value != 'j2':
                            runpoints+=value
                        else:
                            continue
                    tempvalue.append(['points:', runpoints])
                    pointsdict[key].append(tempvalue)


        for dict in possiblesolution['groups']:
            for key in dict.keys():
                for group in dict[key]:
                    grouppoints = 0
                    for value in group:
                        grouppoints += value[1]
                    tempgroup = list(group)
                    tempgroup.append(['points', grouppoints])
                    dict[key] = tempgroup
                    pointsdict['groups'].append(dict)
        return pointsdict

    def find_best_play(self, rack, pointsdict):
        print(f'points: {pointsdict}')
        temprack = rack
        print(f'temprack before loop: {temprack}')
        plays_to_make = defaultdict(list)
        for key in pointsdict.keys():
            if key != 'groups':
                for run in reversed(pointsdict[key]):
                    print(run[0])
                    for tile in run[0]:
                        if tile == 'j1' or tile == 'j2':
                            if tile not in temprack['jokers']:
                                print(f'found {tile}, breaking')
                                break
                            else:
                                temprack['jokers'].remove(tile)
                        elif tile not in temprack[key]:
                            print(f'found {tile} that is not in temprack, breaking')
                            break
                        else:
                            plays_to_make[key] = run[0]
                            temprack[key].remove(tile)

            else:
                for dict in pointsdict[key]:
                    for group in dict.items():
                        print(group)
        print(f'plays we will make: {plays_to_make}')
        print(f'temprack after loop: {temprack}')








