from set_generator import SetGenerator
class SolveTiles:


    def __init__(self):
        pass

    def solve_tiles(self, rack, table):
        print('solve tiles')

    def points(self, possiblesolution):
        points = 0
        for tile in possiblesolution:
            points += tile[0]
        print(points)
        return points
