import sys
import os

# WORD_LIST = [w.strip() for w in open(os.path.join(sys.path[0].replace('/intersects2', ''), "res/words.txt"), "r").readlines()]
# WORD_LIST = [w.strip() for w in open(os.path.join(sys.path[0].replace('/CSP', ''), "res/words.txt"), "r").readlines()]
WORD_LIST = [w.strip() for w in open(os.path.join(sys.path[0].replace('/intersections', ''), "res/words.txt"), "r").readlines()]


def search_words(letters):
    """ Search for a word by using letter constraints.
    Provide a list of letters (in caps), and an empty string for any letter.

    For example: search_words(["H","","L","L",""])
    ['HALLO',
    'HALLS',
    'HELLO',
    'HELLS',
    'HILLO',
    'HILLS',
    'HILLY',
    'HOLLA',
    'HOLLO',
    'HOLLY',
    'HULLO',
    'HULLS',
    'HULLY']
    """
    valid_words = []
    for w in WORD_LIST:
        if len(w) == len(letters):
            valid = True
            for i in range(len(letters)):
                if (letters[i] != "") and (letters[i] != w[i]):
                    valid = False
            if valid:
                valid_words += [w]

    return valid_words


def is_word(letters):
    """ Determine whether or not a list of letters (in caps)
    corresponds to a word in the dictionary.
    example:
    # >>> utils.is_word(["H", "E", "L", "L", "O"])
    True
    # >>> utils.is_word(["H", "E", "L", "L", "P"])
    False
    """
    return "".join(letters) in WORD_LIST


def get_all_words_text():
    return WORD_LIST


def get_init_grid():
    return [[1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],  # 0
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


# def get_init_grid():
#     return [[1, 1, 1, 1, 1],  # 0
#         [0, 0, 1, 0, 1],  # 1
#         [0, 1, 1, 1, 1],  # 2
#         [1, 0, 1, 1, 1],  # 3
#         [1, 1, 1, 1, 1],  # 4
#         [1, 0, 0, 1, 0]]  # 5


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item
