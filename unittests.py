from solve_tiles import SolveTiles

solver = SolveTiles()
tiles = [(1, 1), (2, 1), (3, 1)]
def test_start_new_runs(tiles):
    #hieruit volgen 6 mogelijke combinaties, elke tile enkel, en de unieke combinaties onderling
    solutions = solver.start_new_runs(tiles, 1)
    assert len(solutions) == 6

print(solutions)