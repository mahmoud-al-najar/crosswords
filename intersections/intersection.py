from intersections.word import WordType


def calc_x_y_of_intersect(w1, w2):
    if w1.word_type == WordType.VERTICAL:
        x = w1.raw_indices[0]
        y = w2.raw_indices[0]
        return x, y
    else:
        y = w1.raw_indices[0]
        x = w2.raw_indices[0]
        return x, y


class Intersection:

    def __init__(self, w_x, w_y):
        self.w_x = w_x
        self.w_y = w_y
        self.i_x = w_x.get_textual_index_of_intersect_with(w_y)
        self.i_y = w_y.get_textual_index_of_intersect_with(w_x)
        self.priority = None
        self.l = None
        self.x, self.y = calc_x_y_of_intersect(w_x, w_y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '{\nx: ' + str(self.x) + ', y: ' + str(self.y) + ', l: ' + str(self.l) + ', priority: ' + \
               str(self.priority) + ', \nw_x: ' + str(self.w_x) + ', i_x: ' + str(self.i_x) + \
               '\nw_y: ' + str(self.w_y) + ', i_y: ' + str(self.i_y) + '\n}\n\n'

    def __hash__(self):
        return hash(str(self.x) + '-' + str(self.y))
