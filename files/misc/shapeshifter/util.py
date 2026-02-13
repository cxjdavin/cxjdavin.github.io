# pip3 install ortools jsonpickle
from ortools.constraint_solver import pywrapcp
import jsonpickle
import time

class Timer:
  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, *args):
    self.time_taken = time.time() - self.start

class Pattern:
  def __init__(self, dim, mask):
    assert(len(mask) == dim[0])
    for mask_row in mask:
      assert(len(mask_row) == dim[1])
    self.r, self.c = dim
    self.mask = mask
    self.indicators = dict()

  def add_indicator(self, v, grid_coordinate):
    self.indicators[v] = grid_coordinate

def store_to_file(fname, obj):
  with open(fname, 'w') as fout:
    fout.write(jsonpickle.encode(obj))

def read_from_file(fname):
  obj = None
  with open(fname, 'r') as fin:
    obj = jsonpickle.decode(fin.read())
  return obj
