from util import *

def solve(states, grid, patterns):
  solver = pywrapcp.Solver("problem_instance")
  variables = dict()

  grid_r = len(grid)
  grid_c = len(grid[0])
  grid_vars = []
  for r in range(grid_r):
    grid_vars.append([])
    for c in range(grid_c):
      assert(grid[r][c] in states)
      grid_vars[r].append([])

  indicator_dict = dict()
  indicator_count = 0
  for pattern_id in range(len(patterns)):
    p = patterns[pattern_id]
    for r in range(len(grid)):
      for c in range(len(grid[r])):
        # If p's top left cell can fit at grid[r][c]
        if p.r + r <= grid_r and p.c + c <= grid_c:
          indicator_count += 1
          v = "i_{0}".format(indicator_count)
          p.add_indicator(v, (r,c))
          indicator_dict[indicator_count] = pattern_id
          variables[v] = solver.IntVar(0, 1, v)

          # Fill mask
          for mask_r in range(p.r):
            for mask_c in range(p.c):
              if p.mask[mask_r][mask_c] == 1:
                grid_vars[mask_r + r][mask_c + c].append(v)
  for r in range(grid_r):
    for c in range(grid_c):
      solver.Add((grid[r][c] + solver.Sum([variables[k] for k in grid_vars[r][c]])) % len(states) == 0)
  for p in patterns:
    solver.Add(solver.Sum([variables[k] for k in p.indicators.keys()]) == 1)

  solution = dict()
  db = solver.Phase([v for k,v in variables.items()],
                    solver.CHOOSE_RANDOM,#FIRST_UNBOUND,
                    solver.ASSIGN_RANDOM_VALUE)#MIN_VALUE)

  solver.NewSearch(db)
  solution = []
  while solver.NextSolution():
    for k in range(1, indicator_count + 1):
      v = variables["i_{0}".format(k)]
      solution.append(v.Value())
    print("Solution found")
    break
  solver.EndSearch()
  return solution, indicator_dict

def solution_to_moves(output, indicator_dict, patterns):
  moves = []
  for i in range(len(output)):
    if output[i] == 1:
      indicator_id = i + 1
      pattern_id = indicator_dict[indicator_id]
      pattern = patterns[pattern_id]
      grid_coordinate = pattern.indicators["i_{0}".format(indicator_id)]
      moves.append((pattern_id, grid_coordinate))
  return moves

def main():
  ### Copy-paste output of shapeshifter.js here, then indent once
  level = 36;
  states = [0,1,2];
  grid = [[0, 2, 2, 2, 1, 0],[1, 0, 1, 0, 0, 2],[2, 0, 0, 1, 0, 0],[2, 0, 1, 0, 2, 1],[0, 2, 0, 1, 1, 2],[2, 1, 1, 1, 0, 0]]

  patterns = []
  patterns.append(Pattern((3, 3), [[0, 0, 1],[0, 1, 1],[1, 1, 1]]))
  patterns.append(Pattern((4, 5), [[0, 1, 0, 0, 0],[0, 1, 1, 1, 1],[1, 1, 0, 1, 0],[0, 1, 0, 1, 1]]))
  patterns.append(Pattern((2, 2), [[1, 1],[1, 0]]))
  patterns.append(Pattern((3, 3), [[0, 0, 1],[0, 1, 1],[1, 1, 0]]))
  patterns.append(Pattern((3, 2), [[1, 1],[0, 1],[1, 1]]))
  patterns.append(Pattern((3, 1), [[1],[1],[1]]))
  patterns.append(Pattern((2, 3), [[0, 1, 0],[1, 1, 1]]))
  patterns.append(Pattern((3, 3), [[1, 1, 1],[1, 0, 1],[1, 1, 1]]))
  patterns.append(Pattern((3, 4), [[1, 1, 1, 0],[1, 0, 0, 1],[1, 1, 1, 1]]))
  patterns.append(Pattern((3, 3), [[1, 0, 1],[1, 1, 1],[1, 0, 1]]))
  patterns.append(Pattern((3, 3), [[1, 1, 1],[1, 0, 1],[1, 1, 1]]))
  patterns.append(Pattern((2, 1), [[1],[1]]))
  patterns.append(Pattern((2, 3), [[0, 1, 1],[1, 1, 1]]))
  patterns.append(Pattern((2, 3), [[0, 1, 0],[1, 1, 1]]))
  ### End of copy-paste

  fname = "level{0}.instance".format(level)
  store_to_file(fname, {"level": level,
                        "states": states,
                        "grid": grid,
                        "patterns": patterns})
  print("Stored instance as {0}".format(fname))

  with Timer() as timer:
    solution, indicator_dict = solve(states, grid, patterns)
  print("Solution array: {0}".format(solution))
  moves = solution_to_moves(solution, indicator_dict, patterns)
  print("Moves:")
  for move in moves:
    print(move)
  time_taken = timer.time_taken
  print("Time taken: {0:.2f} seconds".format(time_taken))

  soln_fname = "level{0}.solution".format(level)
  store_to_file(soln_fname, {"level": level,
                             "states": states,
                             "grid": grid,
                             "patterns": patterns,
                             "time_taken": time_taken,
                             "moves": moves,
                             "solver": "ortools"})
  print("Stored solution as {0}".format(soln_fname))

if __name__ == "__main__":
  main()
