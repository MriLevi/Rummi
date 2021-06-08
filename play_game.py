from solve_tiles import SolveTiles
from set_generator import SetGenerator
import random
from collections import defaultdict

def generate_starting_rack(bag):
    '''This function generates a random rack, based off items still left in bag'''
    rack = defaultdict(list)

    for i in range(1, 14):
        #we start by selecting a random key, based on how many values are in a given key
        #this makes sure we still actually draw at random. Instead of each key being 1 in 9 every time
        #we actually have equal odds on every single tile
        random_key = random.choices(list(bag.keys()), weights=[float(len(i)) for i in bag.values()], k=1)
        print(random_key[0])
        while bag[random_key[0]] == []:
            random_key = random.choice(list(bag.keys()))
        random_value = random.choice(bag[random_key[0]])
        rack[random_key[0]].append(random_value)
        bag[random_key[0]].remove(random_value)
    return rack

def main():
    sg = SetGenerator()
    bag = sg.generate_tiles()
    print(f'bag after gen: {bag}')
    rack1 = generate_starting_rack(bag)
    rack2 = generate_starting_rack(bag)
    print(f'bag after rack: {bag}')
main()
from set_generator import SetGenerator


