from enum import Enum
from res.utils import find


class WordType(Enum):

    HORIZONTAL = 1
    VERTICAL = 2


class Word:

    def __init__(self, indices, word_type):
        self.text = None
        self.raw_indices = indices
        self.length = len(indices[1])
        self.intersects = []
        self.word_type = word_type
        self.priority = None
        self.intersect_objects = []

    def __str__(self):
        return '{word_type: ' + str(self.word_type) + ', self.raw_indices[0]: ' + str(self.raw_indices[0]) + \
               ', raw_indices[1]: ' + str(self.raw_indices[1]) + '}'
    # def priority(self):
    #     return len(self.intersects) / len(self.raw_indices[1])

    def calc_intersects(self, all_words):
        for w in all_words:
            if w.word_type != self.word_type:
                if self.raw_indices[0] in w.raw_indices[1] and w.raw_indices[0] in self.raw_indices[1]:
                    self.intersects.append(w)

    def starts_at(self, i):
        return self.raw_indices[1][0] == i

    def ends_at(self, i):
        return self.raw_indices[1][len(self.raw_indices) - 1] == i

    def get_textual_index_of_intersect_with(self, word):
        for i in self.raw_indices[1]:
            if i == word.raw_indices[0]:
                return i - self.raw_indices[1][0]

    def get_grid_index_of_intersect_with(self, word):
        for i in self.raw_indices[1]:
            if i == word.raw_indices[0]:
                return i

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            if self.word_type == other.word_type:
                if self.raw_indices[0] == other.raw_indices[0]:
                    if len(self.raw_indices[1]) == len(other.raw_indices[1]):
                        return True
        return False

    def conforms_with_all_intersects(self, state, text=None):
        for i in self.intersects:
            temp_i = find(lambda ti: ti == i, state.words)
            if temp_i is not None:
                if temp_i.text is not None:
                    x1 = self.get_textual_index_of_intersect_with(temp_i)
                    x2 = temp_i.get_textual_index_of_intersect_with(self)
                    if text is None:
                        text = self.text
                    if text[x1] != temp_i.text[x2]:
                        return False
        return True

    def remove_word_from_intersects(self, last_word):
        for w in self.intersects:
            if w == last_word:
                self.intersects.remove(w)
