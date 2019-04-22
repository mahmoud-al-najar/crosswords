from CSP.constraint import Problem
from CSP import constraint
from CSP.word import Word, WordType
from res.char_grid import make_grid
from res.utils import get_init_grid, is_word


def fill_in_the_blanks(words, keys, solution):
    class FinalState:

        def __init__(self):
            self.words = []
            self.grid = get_init_grid()

        def print_grid(self):
            self.prepare_grid()
            print(make_grid(self.grid))

        def prepare_grid(self):
            for word in self.words:
                if word.word_type == WordType.HORIZONTAL:
                    for i in word.raw_indices[1]:
                        self.grid[word.raw_indices[0]][i] = word.text[i - word.raw_indices[1][0]]
                elif word.word_type == WordType.VERTICAL:
                    for i in word.raw_indices[1]:
                        self.grid[i][word.raw_indices[0]] = word.text[i - word.raw_indices[1][0]]

    final_state = FinalState()
    print()
    for i in range(len(words)):
        w_text = solution.get(keys[i])
        print(w_text, ', valid: ', is_word(list(w_text)))
        words[i].text = w_text
        final_state.words.append(words[i])
    print()
    final_state.print_grid()


def solve(puzzle_words, words_dict):
    import timeit
    problem = Problem()
    # problem.setSolver(constraint.MinConflictsSolver())
    keys = []
    for w in puzzle_words:
        var_id = 'var' + str(w.id)
        dom = words_dict.get(w.length)
        problem.addVariable(variable=var_id, domain=dom)
        keys.append(var_id)

    for w in puzzle_words:
        for i in w.intersects:
            index1 = w.get_textual_index_of_intersect_with(i)
            index2 = i.get_textual_index_of_intersect_with(w)
            v1 = 'var' + str(w.id)
            v2 = 'var' + str(i.id)
            problem.addConstraint(lambda var1, var2, i1=index1, i2=index2: var1[i1] == var2[i2], (v1, v2))

    start_time = timeit.default_timer()
    sol = problem.getSolution()
    end_time = timeit.default_timer()
    print('ELAPSED TIME: ', end_time - start_time)
    fill_in_the_blanks(puzzle_words, keys, sol)
