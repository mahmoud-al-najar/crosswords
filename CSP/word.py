from enum import Enum


class WordType(Enum):

    HORIZONTAL = 1
    VERTICAL = 2


class Word:

    def __init__(self, id, indices, word_type):
        self.id = id
        self.text = None
        # raw meaning that they are based on the grid's indices, not the string's ((they don't have to start from 0))
        self.raw_indices = indices
        self.length = len(indices[1])
        self.intersects = []
        self.word_type = word_type

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

    def conforms_with_all_intersects(self):
        for i in self.intersects:
            x1 = self.get_textual_index_of_intersect_with(i)
            x2 = i.get_textual_index_of_intersect_with(self)
            if i.text is not None:
                    if self.text[x1] != i.text[x2]:
                        return False
        return True

    def remove_word_from_intersects(self, last_word):
        for w in self.intersects:
            if w == last_word:
                self.intersects.remove(w)

    def __hash__(self):
        return hash(tuple(self.__dict__))

    # def __lt__(self, other):
    #     return self.text < other.text
    #
    # def __le__(self, other):
    #     return self.text <= other.text
    #
    # def __gt__(self, other):
    #     return self.text > other.text
    #
    # def __ge__(self, other):
    #     return self.text >= other.text

    def __lt__(self, other):
        return self.length < other.length

    def __le__(self, other):
        return self.length <= other.length

    def __gt__(self, other):
        return self.length > other.length

    def __ge__(self, other):
        return self.length >= other.length
