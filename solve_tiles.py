class SolveTiles:

    def __init__(self, tiles, sets, numbers=13, colors=4, rack=[], table=[]):
        self.tiles=tiles
        self.sets = sets
        self.table = table
        self.rack = rack

    def points(self, possiblesolution):
        points = 0
        for tile in possiblesolution:
            points += tile[0]
        print(points)
        return points
