from intersections.word import Word, WordType
import intersections.astar as astar
import res.utils as utils


def add_all_horizontal_words(words_array):
    for y in range(len(init_grid)):
        x = 0
        while x < len(init_grid[y]) - 1:
            indices = (y, [])
            while init_grid[y][x] != 0:
                indices[1].append(x)
                if x < len(init_grid[y]) - 1:
                    x += 1
                else:
                    break
            if len(indices[1]) > 1:
                word = Word(indices, WordType.HORIZONTAL)
                words_array.append(word)
            x += 1
    return words_array


def add_all_vertical_words(words_array):
    for x in range(len(init_grid[0])):
        y = 0
        while y < len(init_grid):
            indices = (x, [])
            while init_grid[y][x] != 0:
                indices[1].append(y)
                if y < len(init_grid) - 1:
                    y += 1
                else:
                    break
            if len(indices[1]) > 1:
                word = Word(indices, WordType.VERTICAL)
                words_array.append(word)
            y += 1
    return words_array


def get_words_lengths_dictionary(words_array):
    dictionary = dict()
    for word in words_array:
        word_length = len(word)
        if word_length not in dictionary:
            dictionary[word_length] = [word]
        else:
            dictionary.get(word_length).append(word)
    return dictionary


if __name__ == '__main__':

    init_grid = utils.get_init_grid()
    words_dict = get_words_lengths_dictionary(utils.get_all_words_text())
    words = []
    add_all_horizontal_words(words)
    add_all_vertical_words(words)
    for w in words:
        w.calc_intersects(words)
        w.priority = len(w.intersects) / len(w.raw_indices[1])

    astar.solve(words, words_dict)

