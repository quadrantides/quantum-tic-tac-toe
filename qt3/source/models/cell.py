# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""

import random

from qt3.source.constants import NB_CELLS


def get_random_cell():
    return random.randint(0, NB_CELLS-1)


class Cell(object):
    def __init__(self, selectable_cells):
        self.turns = []
        self.is_reduced = False
        self.selectable_cells = selectable_cells

    def reduce(self, turn):
        self.turns = [turn]
        self.is_reduced = True

    def copy(self):
        c = Cell(self.selectable_cells)
        for name in self.turns:
            c.add_turn(name)
        c.is_reduced = self.is_reduced
        return c

    def reinit(self):
        self.turns = []
        self.is_reduced = False

    def is_entangled(self):
        return len(self.turns) > 1

    def remove_turn(self, name):
        self.turns.remove(name)

    def add_turn(self, name):
        if name not in self.turns:
            self.turns.append(name)
        else:
            if len(self.turns) == 1:
                self.turns = [name]
                self.is_reduced = True

    def get_turns(self):
        return self.turns
