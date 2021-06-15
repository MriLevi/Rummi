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
        self.points(sets)
        return runs, rack, board

    def points(self, possiblesolution):

        for run in possiblesolution['runs']:
            print(run)
        for dict in possiblesolution['groups']:
            print(f'dict: {dict}')
            for key in dict.keys():
                print(f'key? {key}')
                for group in dict[key]:
                    print(f'group in dict[key] {group}')
                    grouppoints = 0
                    for value in group:
                        print(f'value : {value}')
                        grouppoints += value[1]
                    tempgroup = list(group)
                    tempgroup.append(['points', grouppoints])
                    print(tempgroup)
                    dict[key] = tempgroup
                    print(dict[key])
                    print(dict)
        points = 0
        return points
