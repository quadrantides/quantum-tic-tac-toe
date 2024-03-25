# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
from bokeh.models.widgets import Button

from qt3.source.models.cell import Cell


class UiCell(Cell):
    def __init__(self, index, entangled_cells, players, parent=None):
        Cell.__init__(self, entangled_cells)
        self.collapse = dict(
            mode=False,
        )
        self.index = index
        self.disabled = False
        self.ui = None
        self.players = players
        self.parent = parent
        self.init()

    def set_collapse_mode(self):
        self.collapse['mode'] = True

    def set_default_mode(self):
        self.collapse['mode'] = False

    def get_metrics(self):
        return [
            "Cell internal values ",
            f"turns : {self.turns}, is_reduced : {self.is_reduced}, disabled : {self.disabled}, index : {self.index}",
        ]

    def on_click(self, event):
        if self.collapse['mode']:
            self.parent.cell_event(self)
        else:
            self.update()

    def init(self):
        self.set_default_mode()
        button_size = 150
        self.ui = Button(label='', width=button_size, height=button_size)
        self.ui.on_click(self.on_click)

    def update(self):
        self.add_turn(
            self.players.get_turn(),
        )
        self.ui.label = " ".join(
            self.get_turns(),
        )
        self.players.increase_active_player_turn_step()
        self.parent.update(self)

    def reinit(self):
        Cell.reinit(self)
        self.ui.label = ""

    def enable(self, save=True):
        if save:
            self.disabled = False
        self.ui.disabled = False

    def disable(self, save=True):
        if save:
            self.disabled = True
        self.ui.disabled = True
