from res.char_grid import make_grid
from third_try.word import WordType
from res.utils import get_init_grid


class State:

    def __init__(self, solved_words):
        self.grid = get_init_grid()
        self.words = solved_words
        # self.g = None
        self.g = 0
        self.h = None
        self.f = None
    #     self.last_word_added = None
    #
    # def set_last_word(self, word):
    #     self.last_word_added = word
    #
    #     if word.word_type == WordType.HORIZONTAL:
    #         for i in word.raw_indices[1]:
    #             self.grid[word.raw_indices[0]][i] = word.text[i - word.raw_indices[1][0]]
    #     elif word.word_type == WordType.VERTICAL:
    #         for i in word.raw_indices[1]:
    #             self.grid[i][word.raw_indices[0]] = word.text[i - word.raw_indices[1][0]]

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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
            # \
            #        and any(x in other.words for x in self.words) \
            #        and any(x in self.words for x in other.words)
        return False

    def words_to_string(self):
        s = '('
        for w in self.words:
            s += w.text + ' - '
        s = s[:-3]
        s += ')'
        return s
