# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
from qt3.source.constants import NEIGHBOR_CELLS


def is_cell_indexes_sequence_collapsible(cell_indexes_value):
    return cell_indexes_value[0] == cell_indexes_value[-1] if len(cell_indexes_value) > 2 else False


class Collapse(object):

    def __init__(self, cells):
        self.cells = cells
        self.current_turns_sequence = []
        self.current_cell_indexes_sequence = []

    def get_data(self):
        return dict(
            turns_sequence=self.current_turns_sequence,
            cell_indexes_sequence=self.current_cell_indexes_sequence,

        )

    def init(self):
        self.current_turns_sequence = []
        self.current_cell_indexes_sequence = []

    def find_next_collapsible_cell_indexes_sequence(self, cells, cell_index=0):
        found = False
        cell = cells[cell_index]
        cell_index_turns = cell.get_turns()
        if cell_index_turns:
            cell_index_turn = cell_index_turns[0]
            cell.remove_turn(cell_index_turn)
            self.current_cell_indexes_sequence.append(cell_index)
            self.current_turns_sequence.append(cell_index_turn)

            selectable_cell_indices = NEIGHBOR_CELLS[cell_index]
            j = 0
            nb_selectable_cells = len(selectable_cell_indices)
            eodj = j >= nb_selectable_cells

            while not found and not eodj:
                selectable_cell_index = selectable_cell_indices[j]
                selectable_cell_turns = cells[selectable_cell_index].get_turns()
                if cell_index_turn in selectable_cell_turns:
                    self.current_turns_sequence.append(cell_index_turn)
                    self.current_cell_indexes_sequence.append(selectable_cell_index)
                    if is_cell_indexes_sequence_collapsible(self.current_cell_indexes_sequence):
                        found = True
                    else:
                        selectable_cell_turns.remove(cell_index_turn)
                        if selectable_cell_turns:
                            found = self.find_next_collapsible_cell_indexes_sequence(
                                cells,
                                cell_index=selectable_cell_index,
                            )

                if not found:
                    j += 1
                eodj = j >= nb_selectable_cells

        return found

    def cells_copy(self):
        copy = []
        for cell in self.cells:
            copy.append(cell.copy())
        return copy

    def has_collapsible_sequence(self):
        return is_cell_indexes_sequence_collapsible(self.current_cell_indexes_sequence)

    def get_collapsible_sequence(self):
        return self.current_turns_sequence

    def get_collapsible_cell_indexes_sequence(self):
        return self.current_cell_indexes_sequence

    def collapse_sequence(self, index, first_turn):
        current_index = self.current_cell_indexes_sequence.index(index)
        indexes = \
            self.current_cell_indexes_sequence[current_index::] + self.current_cell_indexes_sequence[0:current_index]
        turns = self.current_turns_sequence[current_index::] + self.current_turns_sequence[0:current_index]

        if indexes[0] == indexes[-1]:
            indexes.insert(0, indexes[-1])
            indexes.pop()
            turns.insert(0, turns[-1])
            turns.pop()

        nb_turns = len(turns)
        chunked_turns = [turns[x:x + 2] for x in range(0, nb_turns, 2)]
        chunked_indexes = [indexes[x:x + 2] for x in range(0, nb_turns, 2)]

        collapsed_indexes = []
        collapsed_turns = []

        w_turn = first_turn
        for i in range(len(chunked_turns)):
            turns_i = chunked_turns[i]
            indexes_i = chunked_indexes[i]
            collapsed_index = turns_i.index(w_turn)
            if collapsed_index == -1:
                break
            else:
                collapsed_turn = turns_i[collapsed_index]
                other_chunked_index = 1 - collapsed_index

                collapsed_turns.append(collapsed_turn)
                collapsed_indexes.append(indexes_i[collapsed_index])
                # Re-initialization for next loop
                w_turn = turns_i[other_chunked_index]

        # update ui cells
        for c_index, c_turn in zip(collapsed_indexes, collapsed_turns):
            self.cells[c_index].ui.label = c_turn
            self.cells[c_index].reduce(c_turn)

    def message(self):
        return "ok"

    def execute(self):
        found = False
        i = 0
        nb_cells = len(self.cells)
        eod = i >= nb_cells

        while not found and not eod:
            cells = self.cells_copy()
            if self.find_next_collapsible_cell_indexes_sequence(cells, cell_index=i):
                found = True
            else:
                i += 1
                self.init()
            eod = i >= nb_cells


if __name__ == '__main__':
    from qt3.source.view.game import UiCells
    # case = {
    #     0: ["X1", "O4"],
    #     3: ["O2", "O4"],
    #     4: ["X1", "O2", "X3"],
    #     8: ["X3"],
    # }
    # case = {
    #     6: ["X3", "O2"],
    #     3: ["O2", "X3"],
    #     4: ["X1"],
    # }
    case = {
        7: ["X3", "O4"],
        8: ["O4", "X3"],
        0: ["X1"],
    }

    game = UiCells()
    game.load(case)
    process = Collapse(game.cells)
    process.execute()
    simulated_index = 8
    first_turn = "X3"
    process.collapse_sequence(simulated_index, first_turn)

