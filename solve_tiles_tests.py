import unittest
from solve_tiles import SolveTiles

class TestSolveTiles(unittest.TestCase):

    def setUp(self):
        self.solver = SolveTiles()

    def test_start_new_runs(self):
        tiles = [(1,1), (2,1), (3,1)]
        n = 1
        runs = self.solver.start_new_runs(tiles, n)
        runs_wrong_n = self.solver.start_new_runs(tiles, n+1)
        #here we expect to see [(1,1)], [(2,1)], [(3,1)], [[(1,1)] [(2,1)], [[(1,1)] [(3,1)]] and [[(2,1)] [[(3,1)]]
        #so 6 solutions.
        self.assertEqual(len(runs), 6, 'runs are not correct length!')
        #since we have only n=1 tiles, we should expect 0 new runs to be started
        self.assertEqual(len(runs_wrong_n), 0, 'we have made runs without tiles of n value!')

    def test_find_new_groups(self):
        tiles = [(1, 1), (2, 1), (3, 1), (4,1)]
        n = 1
        groups = self.solver.find_new_groups(n, tiles)

        #we should find one group of 4, and 4 unique groups of 3. Meaning we find 5 solutions.
        self.assertEqual(len(groups), 5)

    def test_start_new_runs(self):
        tiles = [(1, 1), (2, 1), (3, 1), (4,1)]
        n = 1
        new_runs = self.solver.start_new_runs(tiles, n)
        #this function should make new solutions where it starts new runs for every tile with n value
        #it should also make new solutions for every combination of tiles as new run starts
        #so [(1,1)], [(2,1)], [(3,1)] and [(4,1)],
        #but also combinations like [[(1,1)] [(2,1)]] and [[(1,1)] [(2,1)] [(4,1)]
        #a total of 15 solutions is expected from a 4 length list

        self.assertEqual(len(new_runs), 15)

    def test_canExtend(self):
        tile1 = (3,1)
        tile2 = (5,'j1')
        tile3 = (3,2)
        tile4 = (3,3)
        tile5 = (4,2)
        set = [(3,1)]

        # this set is extendable by any joker, by the tile (3,2). Any other tile should return false.
        eval1 = self.solver.can_extend(tile1, set) # test if equal tile extends
        eval2 = self.solver.can_extend(tile2, set) # test if
        eval3 = self.solver.can_extend(tile3, set)
        eval4 = self.solver.can_extend(tile4, set)
        eval5 = self.solver.can_extend(tile5, set)

        set2 = [(3, 1), (3, 2)]
        eval6 = self.solver.can_extend(tile1, set2)
        eval7 = self.solver.can_extend(tile2, set2)
        eval8 = self.solver.can_extend(tile4, set2)

        self.assertEqual(eval1, False)
        self.assertEqual(eval2, True)
        self.assertEqual(eval3, True)
        self.assertEqual(eval4, False)
        self.assertEqual(eval5, False)
        self.assertEqual(eval6, False)
        self.assertEqual(eval7, True)
        self.assertEqual(eval8, True)

    def test_is_set_group(self):

        set1=[(1, 1), (2, 1), (3, 1), (4, 1)] #this is a 4 length group
        set2=[(1,1), (2,1), (3,1)] #3 length
        set3=[(1,1), (2,1)] #2 length isnt a group
        set4=[(1,1), (1,2), (1,3)] #this is a run

        self.assertEqual(self.solver.is_set_group(set1), True)
        self.assertEqual(self.solver.is_set_group(set2), True)
        self.assertEqual(self.solver.is_set_group(set3), False)
        self.assertEqual(self.solver.is_set_group(set4), False)

    def test_calculate_score(self):

        set1 = [[(1, 1), (2, 1), (3, 1), (4, 1)]] #expected score = 4
        set2 = [[(1, 13), (2, 13), (3, 13)]]      #expected score = 39
        set3 = [[(1, 13), (2, 13), (3, 13)], [(1, 1), (2, 1), (3, 1), (4, 1)]] #expected score, 43
        set4 = [[(1, 13), (2, 13)], [(1, 1), (2, 1), (3, 1), (4, 1)]] #expected score 0 because of invalid group

        self.assertEqual(self.solver.calculate_score(set1), 4)
        self.assertEqual(self.solver.calculate_score(set2), 39)
        self.assertEqual(self.solver.calculate_score(set3), 43)
        self.assertEqual(self.solver.calculate_score(set4), 0)


