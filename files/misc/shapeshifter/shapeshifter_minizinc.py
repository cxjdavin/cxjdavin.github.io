from util import *
import subprocess

def stringify(arr):
  result = ""
  for i in range(len(arr)):
    result += arr[i]
    if i < len(arr) - 1:
      result += " + "
  return result
'''
def count_min_cell_toggles(grid, states):
  count = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      count += 0 if grid[i][j] == 0 else len(states) - grid[i][j]
  return count

def count_pattern_cell_toggles(patterns):
  count = 0
  for pattern in patterns:
    for i in range(len(pattern.mask)):
      for j in range(len(pattern.mask[i])):
        count += pattern.mask[i][j]
  return count
'''
def create_minizinc(mzn_fname, states, grid, patterns):
  grid_r = len(grid)
  grid_c = len(grid[0])
  grid_vars = []
  for r in range(grid_r):
    grid_vars.append([])
    for c in range(grid_c):
      assert(grid[r][c] in states)
      grid_vars[r].append([str(grid[r][c])])

  #min_toggles = count_min_cell_toggles(grid, states)
  #pat_toggles = count_pattern_cell_toggles(patterns)
  #print(min_toggles, pat_toggles)
  max_cycles = 2;

  indicator_dict = dict()
  indicator_count = 0
  with open(mzn_fname, 'w') as fout:
    fout.write("int: max_cycles = {0};\n".format(max_cycles))
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
            fout.write("var bool: i_{0};\n".format(indicator_count))

            # Fill mask
            for mask_r in range(p.r):
              for mask_c in range(p.c):
                if p.mask[mask_r][mask_c] == 1:
                  grid_vars[mask_r + r][mask_c + c].append(v)

    all_indicators_string = "array[int] of var int: I = ["
    for i in range(1, indicator_count+1):
      all_indicators_string += "i_{0}".format(i)
      if i < indicator_count:
        all_indicators_string += ", "
      else:
        all_indicators_string += "];\n"
    fout.write(all_indicators_string)

    for r in range(grid_r):
      for c in range(grid_c):
        sum_string = stringify(grid_vars[r][c])
        fout.write("constraint ({0}) mod {1} = 0;\n".format(sum_string, len(states)))
        fout.write("constraint ({0}) <= max_cyles * {2};\n".format(sum_string, len(states)))

    for p in patterns:
      sum_string = stringify(list(p.indicators.keys()))
      fout.write("constraint {0} = 1;\n".format(sum_string))

    fout.write("solve satisfy;\n")
    fout.write("output [\"\(I)\"];\n")
  return indicator_dict

def solve_minizinc(mzn_fname):
  cmd = "minizinc {0} -o {0}.out".format(mzn_fname)
  subprocess.call(cmd, shell=True)

  solution = []
  with open("{0}.out".format(mzn_fname), 'r') as fin:
    line = fin.readline()
    solution = [int(x[0]) for x in line[1:].split()]
  return solution

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
  level = 46;
  states = [0,1,2];
  grid = [[0, 0, 0, 0, 2, 0, 0],[0, 0, 0, 1, 2, 2, 0],[0, 0, 1, 0, 0, 2, 0],[0, 1, 2, 2, 0, 2, 2],[2, 1, 2, 2, 1, 0, 0],[0, 1, 0, 0, 0, 1, 2],[0, 0, 0, 2, 1, 2, 2],[0, 2, 0, 0, 2, 2, 2]]

  patterns = []
  patterns.append(Pattern((4, 5), [[1, 1, 0, 1, 1],[0, 1, 1, 0, 1],[0, 0, 1, 1, 1],[1, 1, 1, 0, 0]]))
  patterns.append(Pattern((3, 3), [[1, 1, 0],[0, 1, 1],[1, 1, 0]]))
  patterns.append(Pattern((3, 2), [[1, 1],[0, 1],[1, 1]]))
  patterns.append(Pattern((3, 2), [[0, 1],[1, 1],[0, 1]]))
  patterns.append(Pattern((4, 4), [[1, 1, 1, 0],[0, 0, 1, 1],[1, 1, 1, 0],[0, 1, 0, 0]]))
  patterns.append(Pattern((4, 3), [[0, 1, 0],[1, 1, 0],[0, 1, 1],[0, 1, 0]]))
  patterns.append(Pattern((3, 4), [[1, 0, 0, 1],[1, 0, 1, 1],[1, 1, 1, 1]]))
  patterns.append(Pattern((3, 3), [[0, 1, 1],[0, 1, 0],[1, 1, 0]]))
  patterns.append(Pattern((2, 3), [[0, 1, 0],[1, 1, 1]]))
  patterns.append(Pattern((4, 4), [[1, 1, 0, 0],[1, 0, 0, 0],[1, 0, 1, 0],[1, 1, 1, 1]]))
  patterns.append(Pattern((2, 2), [[1, 1],[1, 0]]))
  patterns.append(Pattern((2, 1), [[1],[1]]))
  patterns.append(Pattern((3, 4), [[0, 1, 0, 0],[1, 1, 0, 1],[0, 1, 1, 1]]))
  patterns.append(Pattern((2, 2), [[1, 0],[1, 1]]))
  patterns.append(Pattern((4, 3), [[0, 1, 0],[1, 1, 0],[0, 1, 1],[0, 1, 0]]))
  patterns.append(Pattern((4, 3), [[1, 1, 0],[1, 0, 0],[1, 1, 1],[0, 0, 1]]))
  ### End of copy-paste

  fname = "level{0}.instance".format(level)
  store_to_file(fname, {"level": level,
                        "states": states,
                        "grid": grid,
                        "patterns": patterns})
  print("Stored instance as {0}".format(fname))

  with Timer() as timer:
    mzn_fname = "level{0}.mzn".format(level)
    indicator_dict = create_minizinc(mzn_fname, states, grid, patterns)
    #solution = solve_minizinc(mzn_fname)
    #solution =
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
                             "solver": "minizinc"})
  print("Stored solution as {0}".format(soln_fname))

if __name__ == "__main__":
  main()
