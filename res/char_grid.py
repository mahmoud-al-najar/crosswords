import string
import numpy as np

GRID = [[1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],  # 0
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],  # 1
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],  # 2
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],  # 3
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],  # 4
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],  # 6
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],  # 7
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],  # 8
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],  # 9
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1]]  # 10


def random_index_grid():
    ab = list(string.ascii_uppercase)
    rgrid = np.random.randint(1, len(ab)+1, (11, 11))
    inds = rgrid * GRID
    return inds


def make_grid(inds):
    ab = [" "] + list(string.ascii_uppercase)
    grid_letters = [" "]
    for row in inds:
        for col in row:
            # grid_letters += [ab[col]]
            grid_letters += [str(col)]
        grid_letters += ["\n"]

    grid = " ".join(grid_letters)
    return grid[1:]


def draw_random_example():
    inds = random_index_grid()
    print(make_grid(inds))


if __name__ == "__main__":
    draw_random_example()

