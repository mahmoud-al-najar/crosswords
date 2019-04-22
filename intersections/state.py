from res.char_grid import make_grid
from res.utils import get_init_grid


class State:

    def __init__(self):
        self.solved_intersects = []
        self.picked_words = []
        self.g = 0
        self.h = None
        self.f = None

    def print_grid(self):
        grid = self.prepare_grid(get_init_grid())
        print(make_grid(grid))

    def prepare_grid(self, grid):
        for intersect in self.solved_intersects:
            grid[intersect.y][intersect.x] = intersect.l
        return grid

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):

            if not len(self.solved_intersects) == len(other.solved_intersects):
                return False
            else:
                for i in range(len(self.solved_intersects)):
                    if not self.solved_intersects[i] == other.solved_intersects[i]:
                        return False
                    elif not self.solved_intersects[i].l == other.solved_intersects[i].l:
                        return False
            return True

        return False
