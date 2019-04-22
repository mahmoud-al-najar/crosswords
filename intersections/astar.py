from intersections.state import State
from intersections.word import WordType
from intersections.intersection import Intersection
import copy
from res.utils import get_init_grid, is_word
from res.char_grid import make_grid
import timeit

MASTER_DICT = None


def fill_in_the_blanks(words, current):
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
    picked_words = []
    for w in words:
        relevant_intersects = []
        for i in current.solved_intersects:
            if i in w.intersect_objects:
                relevant_intersects.append(i)
        if w.word_type == WordType.HORIZONTAL:
            possible_words = list(get_words_for_x_intersects(relevant_intersects))
        else:
            possible_words = list(get_words_for_y_intersects(relevant_intersects))
        for pw in possible_words:
            if pw not in picked_words:
                w.text = pw
                picked_words.append(pw)
                break

    for w in words:
        if w.text is None:
            return False

    for w in words:
        final_state.words.append(w)
    final_state.print_grid()

    picked_words.sort(key=lambda w: len(w))
    for w in picked_words:
        print(w, ' -- valid: ', is_word(list(w)))
    return True


def solve(puzzle_words, all_words_dict):
    global MASTER_DICT
    MASTER_DICT = prepare_exhaustive_dict(all_words_dict)
    print('----------DICTIONARY IS READY----------')

    start_time = timeit.default_timer()

    # --------- INIT ---------
    empty_intersects = []
    for w in puzzle_words:
        w.priority = len(all_words_dict.get(w.length))

    for w in puzzle_words:
        for i in w.intersects:
            if w.word_type == WordType.HORIZONTAL:
                intersect = Intersection(w_x=w, w_y=i)
            else:
                intersect = Intersection(w_x=i, w_y=w)
            intersect.priority = w.priority + i.priority
            w.intersect_objects.append(intersect)
            if intersect not in empty_intersects:
                empty_intersects.append(intersect)

    empty_intersects.sort(key=lambda x: x.priority, reverse=False)
    print('len(empty_intersects): ', len(empty_intersects))

    for i in empty_intersects:
        print(i)

    init_intersect = copy.deepcopy(empty_intersects[0])
    w_x = init_intersect.w_x
    w_y = init_intersect.w_y
    w_x_poss = all_words_dict.get(w_x.length)
    w_y_poss = all_words_dict.get(w_y.length)

    init_poss_l_x = []
    init_poss_l_y = []
    for p in w_x_poss:
        if p[init_intersect.i_x] not in init_poss_l_x:
            init_poss_l_x.append(p[init_intersect.i_x])
    for p in w_y_poss:
        if p[init_intersect.i_y] not in init_poss_l_y:
            init_poss_l_y.append(p[init_intersect.i_y])

    common_init_possibilities = list(set(init_poss_l_x) & set(init_poss_l_y))

    open_set = []
    closed_set = []

    for p in common_init_possibilities:
        temp_state = State()
        temp_intersect = copy.deepcopy(init_intersect)
        temp_intersect.l = p
        temp_state.solved_intersects.append(temp_intersect)
        temp_state.g = 0
        temp_state.h = heuristic(temp_state)
        temp_state.f = temp_state.g + temp_state.h
        open_set.append(temp_state)

    while len(open_set) > 0:
        current = get_state_with_maximum_f(open_set)
        print(len(open_set))
        print(len(current.solved_intersects))
        print(current.picked_words)
        current.print_grid()

        while len(current.solved_intersects) == len(empty_intersects):
            solved = fill_in_the_blanks(current=current, words=puzzle_words)
            if solved:
                print('\n**********DONE**********\n')
                end = timeit.default_timer()
                elapsed_time = end - start_time
                print('TIME: ', elapsed_time)
                quit()
            else:
                print('NOT SOLVED')
                closed_set.append(current)
                open_set.remove(current)
                current = get_state_with_maximum_f(open_set)
                print(len(current.solved_intersects))
                current.print_grid()

        closed_set.append(current)
        open_set.remove(current)

        next_intersect = get_next_important_intersect(current, empty_intersects)

        relevant_intersects_x = []
        relevant_intersects_y = []
        for i in current.solved_intersects:
            if i.x == next_intersect.x:
                if i in next_intersect.w_y.intersect_objects:
                    relevant_intersects_y.append(i)
            elif i.y == next_intersect.y:
                if i in next_intersect.w_x.intersect_objects:
                    relevant_intersects_x.append(i)

        if len(relevant_intersects_x) > 0:
            poss_w_x = get_words_for_x_intersects(relevant_intersects_x)
        else:
            poss_w_x = all_words_dict.get(next_intersect.w_x.length)
        if len(relevant_intersects_y) > 0:
            poss_w_y = get_words_for_y_intersects(relevant_intersects_y)
        else:
            poss_w_y = all_words_dict.get(next_intersect.w_y.length)

        for w in current.picked_words:
            if w in poss_w_x:
                poss_w_x.remove(w)
            if w in poss_w_y:
                poss_w_y.remove(w)

        poss_next_intersect_x = []
        poss_next_intersect_y = []
        for p in poss_w_x:
            if p[next_intersect.i_x] not in poss_next_intersect_x:
                poss_next_intersect_x.append(p[next_intersect.i_x])
        for p in poss_w_y:
            if p[next_intersect.i_y] not in poss_next_intersect_y:
                poss_next_intersect_y.append(p[next_intersect.i_y])
        poss_next_intersect = list(set(poss_next_intersect_x) & set(poss_next_intersect_y))

        if len(poss_next_intersect) > 0:
            for p in poss_next_intersect:
                # print(p)
                temp_state = copy.deepcopy(current)
                temp_intersect = copy.deepcopy(next_intersect)
                temp_intersect.l = p
                temp_state.solved_intersects.append(temp_intersect)
                temp_state.g = current.g + 1
                temp_state.h = heuristic(temp_state)
                temp_state.f = temp_state.g + temp_state.h
                if temp_state not in closed_set and temp_state not in open_set:
                    words = check_solved_words(temp_state, puzzle_words)
                    for w in words:
                        rel_intersects = []
                        for i in temp_state.solved_intersects:
                            if i in w.intersect_objects:
                                rel_intersects.append(i)
                        if w.word_type == WordType.HORIZONTAL:
                            w_text = list(get_words_for_x_intersects(rel_intersects))[0]
                        else:
                            w_text = list(get_words_for_y_intersects(rel_intersects))[0]

                        if w_text not in temp_state.picked_words:
                            temp_state.picked_words.append(w_text)
                    open_set.append(temp_state)
    print('no solution')


def get_words_for_x_intersects(intersects):
    main_poss_list = []  # contains multiple lists, list_n contains possibilities for intersect_n
    for i in intersects:
        key = str(i.w_x.length) + '-' + str(i.i_x) + '-' + i.l
        poss_list = MASTER_DICT.get(key)
        main_poss_list.append(set(poss_list))
    return set.intersection(*main_poss_list)


def get_words_for_y_intersects(intersects):
    main_poss_list = []
    for i in intersects:
        key = str(i.w_y.length) + '-' + str(i.i_y) + '-' + i.l
        poss_list = MASTER_DICT.get(key)
        main_poss_list.append(set(poss_list))
    return set.intersection(*main_poss_list)


def prepare_exhaustive_dict(all_words_dict):
    new_dict = dict()
    for length in all_words_dict.keys():
        words = all_words_dict.get(length)
        for w_text in words:
            for i in range(len(w_text)):
                l = w_text[i]
                key = str(length) + '-' + str(i) + '-' + l
                if key not in new_dict:
                    new_dict[key] = []
                new_dict[key].append(w_text)
    return new_dict


def heuristic(state):
    h = 0
    for i in state.solved_intersects:
        key1 = str(i.w_x.length) + '-' + str(i.w_x.get_textual_index_of_intersect_with(i.w_y)) + '-' + i.l
        poss_for_w_x = MASTER_DICT.get(key1)
        key2 = str(i.w_y.length) + '-' + str(i.w_y.get_textual_index_of_intersect_with(i.w_x)) + '-' + i.l
        poss_for_w_y = MASTER_DICT.get(key2)
        h += len(poss_for_w_x)
        h += len(poss_for_w_y)
    return h


def get_state_with_maximum_f(open_set):
    temp = open_set[0]
    for s in open_set:
        if s.f > temp.f:
            temp = s
    return temp


def get_next_important_intersect(state, empty_intersects):
    for i in empty_intersects:
        if i not in state.solved_intersects:
            return i


def check_solved_words(state, puzzle_words):
    solved_words = []
    for w in puzzle_words:
        if set(w.intersect_objects).issubset(set(state.solved_intersects)):
            solved_words.append(w)
    return solved_words
