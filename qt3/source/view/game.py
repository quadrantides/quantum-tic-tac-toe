# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
import random
from bokeh.models.widgets import Button
from bokeh.models.widgets import Div
from bokeh.layouts import column, row

from qt3.source.constants import NB_CELLS
from qt3.source.constants import WINNING_COMBINATIONS
from qt3.source.constants import SELECTABLE_CELLS_SCOPE

from qt3.source.models.player import Players
from qt3.source.process import Collapse as CollapseProcess

from qt3.source.view.cell import UiCell

DEFAULT_USER_MESSAGE = "You are the active PLAYER. Click on cells"

DEBUG = False


def is_winning_combination(cells):
    players = []
    for cell in cells:
        if cell.is_reduced:
            turns = cell.get_turns()
            if len(turns) == 1:
                players.append(turns[0][0])
    return len(players) == 3 and len(set(players)) == 1


def get_player_to_collapse_sequence(sequence):
    indexes = [turn[1] for turn in sequence]
    index = indexes.index(min(indexes))
    return sequence[index][0]


def get_first_turn_for_collapse(sequence):
    indexes = [turn[1] for turn in sequence]
    index = indexes.index(min(indexes))
    return sequence[index]


def get_random_cell():
    return random.randint(0, NB_CELLS-1)


class UiCells(object):
    def __init__(self):
        self.ui = dict(
            description=Div(
                text=
                "<h3>"
                "<span>You are the <strong>X player</strong>"
                "</span>"
                " and you are the first to play."
                "</h3>",
            ),
            button_restart=Button(label="Restart"),
            button_get_o_player_turn=Button(label="Player O Run", disabled=True, button_type="success"),
            button_collapse=Button(label="Player O Collapse", disabled=True, button_type="success"),
            user_message_line1=Div(text=""),
            user_message_line2=Div(text=""),
        )
        self.cells = []
        self.players = Players()
        self.collapse = dict()
        self.init()

    def set_collapse_mode(self, player):
        self.collapse["player"] = player
        for cell in self.cells:
            cell.set_collapse_mode()

    def set_default_mode(self):
        for cell in self.cells:
            cell.set_default_mode()

    def button_get_o_player_turn_event(self):
        random_cell_i = get_random_cell()
        max_attempts = 10
        attempts = 0
        eod = attempts >= max_attempts
        while self.cells[random_cell_i].is_reduced and not eod:
            random_cell_i = get_random_cell()
            attempts += 1
        if DEBUG:
            random_cell_i = 4
        if not eod:
            # 1st click simulation on the corresponding cell
            self.cells[random_cell_i].on_click(None)

            random_cell_j = get_random_cell()
            max_attempts = 10
            attempts = 0
            eod = attempts >= max_attempts
            while (
                    self.cells[random_cell_j].is_reduced or
                    random_cell_j not in self.cells[random_cell_i].selectable_cells
            ) and not eod:
                random_cell_j = get_random_cell()
                attempts += 1
            if DEBUG:
                random_cell_j = 8
            if not eod:
                # 2nd click simulation on the corresponding cell
                self.cells[random_cell_j].on_click(None)

    def inform_player_has_changed(self, player):
        msg = f"{player} is now the active PLAYER" if player == "O" else DEFAULT_USER_MESSAGE
        self.ui["user_message_line1"].text = f"<h3 class='user-message'>{msg}</h3>"
        if player == "O":
            text2 = \
                "<h3>" \
                "Player O mandates Player X to click the 'Player O Run' button" \
                "</h3>"
        else:
            text2 = \
                "<h3>" \
                "Click twice on the same cell or on two different cells" \
                "</h3>"

        self.ui["user_message_line2"].text = text2

    def inform_current_player_metrics(self):
        metrics = self.players.get_active_player_metrics()
        self.ui["user_message_line1"].text = f"<h3 class='user-message'>{metrics[0]}</h3>"
        self.ui["user_message_line2"].text = f"<h3 class='user-message'>{metrics[1]}</h3>"

    def inform_current_cell_metrics(self, cell):
        metrics = cell.get_metrics()
        self.ui["user_message_line1"].text = f"<h3 class='user-message'>{metrics[0]}</h3>"
        self.ui["user_message_line1"].text = f"<h3 class='user-message'>{metrics[1]}</h3>"

    def inform_about_end_of_game(self, winner):
        self.ui["user_message_line1"].text = \
            "<span style='font-size:20px;color: #00990d;'>" \
            f"Congratulations {winner}, you win the game !" \
            "</span>"
        msg = "Click on 'Start' to play again"
        self.ui["user_message_line2"].text = f"<h3 class='user-message'>{msg}</h3>"

    def inform_about_selected_cell_for_collapse(self, cell):
        metrics = cell.get_metrics()
        self.ui["user_message_line1"].text = \
            f"<h3 style='font-size:20px;color: #99000d;>" \
            f"{metrics[0]}" \
            f"</h3>"
        self.ui["user_message_line2"].text = \
            f"<h3>" \
            f"{metrics[1]}" \
            f"</h3>"

    def inform_player_to_collapse_sequence(self, process, player):
        sequence = process.get_collapsible_sequence()
        if player == "O":
            text1 = \
                "<h3>" \
                f"Collapsible sequence for Player O" \
                "</h3>"
            text2 = \
                "<h3>" \
                "Player O mandates Player X to click the 'Player O Collapse' button" \
                "</h3>"
        else:
            text1 = \
                "<h3>" \
                f"Collapsible sequence for Player X" \
                "</h3>"
            text2 = \
                "<h3>" \
                "The collapse is depending on your choice, click on a cell" \
                "</h3>"

        self.ui["user_message_line1"].text = text1
        self.ui["user_message_line2"].text = text2

    def button_collapse_event(self, event):
        pass

    def init(self):
        self.inform_player_has_changed("X")
        self.ui["button_get_o_player_turn"].on_click(self.button_get_o_player_turn_event)
        self.ui["button_collapse"].on_click(self.button_collapse_event)

        self.ui["button_restart"].on_click(self.restart)
        for i in range(NB_CELLS):
            self.cells.append(
                UiCell(
                    i,
                    SELECTABLE_CELLS_SCOPE[i],
                    self.players,
                    parent=self,
                )
            )

        self.collapse = dict(
            process=CollapseProcess(self.cells),
            player="",
        )

    def load(self, case):
        for i in case.keys():
            turns = case[i]
            for turn in turns:
                self.cells[i].add_turn(turn)

    def get_cell(self, model_id):
        eod = False
        found = 0
        i = 0

        while not found and not eod:
            cell = self.cells[i]
            if cell.id == model_id:
                found = True
            else:
                i += 1
            if i == NB_CELLS:
                eod = True
        if not found:
            cell = None
        return cell

    def get_layout(self):
        cells_ui = self.get_cells_ui()
        board_layout = row(
            column(*cells_ui[0:3]),
            column(*cells_ui[3:6]),
            column(*cells_ui[6:9]),
        )
        layout = column(
            self.ui["description"],
            self.ui["user_message_line1"],
            self.ui["user_message_line2"],
            self.ui["button_restart"],
            row(
                self.ui["button_get_o_player_turn"],
                self.ui["button_collapse"],
                width=475,
            ),
            board_layout,
        )
        return layout

    def get_cells_ui(self):
        uis = []
        for cell in self.cells:
            uis.append(
                cell.ui,
            )
        return uis

    def update(self, cell):
        winner = ""
        active_player = self.players.get_active_player()
        if DEBUG:
            # self.inform_current_player_metrics()
            self.inform_current_cell_metrics(cell)

        self.enable()
        if active_player.is_first_turn():
            # Update Cells appearance
            self.disable_forbidden_cells(cell)
        elif active_player.is_second_turn():
            winner = self.get_winner()
            if winner:
                self.disable()
                self.inform_about_end_of_game(winner)
            else:
                # Update Cells appearance
                self.disable_reduced_cells()
                # Next player
                self.players.next_player()
                active_player = self.players.get_active_player()
                self.inform_player_has_changed(active_player.name)

        if not winner:
            # Update 'player O' button
            self.ui["button_get_o_player_turn"].disabled = False if self.players.is_o_active_player() else True
            if self.players.is_o_active_player():
                # To avoid player X from clicking on any cells
                self.disable()

        # Search and collapse entangled sequences
        process = self.collapse["process"]
        process.execute()
        if process.has_collapsible_sequence():
            # Now it's collapse mode
            sequence = process.get_collapsible_sequence()
            player = get_player_to_collapse_sequence(sequence)
            self.set_collapse_mode(player)
            self.inform_player_to_collapse_sequence(
                process,
                player,
            )

            self.disable(save=False)
            cell_indexes = set(process.get_collapsible_cell_indexes_sequence())
            for cell_index in cell_indexes:
                self.cells[cell_index].enable(save=False)

    def cell_event(self, cell):
        if cell.collapse["mode"]:
            if DEBUG:
                self.inform_about_selected_cell_for_collapse(cell)
            process = self.collapse["process"]
            process.execute()
            sequence = process.get_collapsible_sequence()

            process.collapse_sequence(
                cell.index,
                get_first_turn_for_collapse(sequence),
            )

            # return to the default mode
            cell_indexes = set(process.get_collapsible_cell_indexes_sequence())
            # retrieve the default mode
            for cell_index in cell_indexes:
                if self.cells[cell_index].disabled:
                    self.cells[cell_index].disable(save=False)
                else:
                    self.cells[cell_index].enable(save=False)
            # Update Cells appearance
            self.disable_reduced_cells()
            self.set_default_mode()

    def get_winner(self):
        found = False
        i = 0
        nb_combinations = len(WINNING_COMBINATIONS)
        eod = i >= nb_combinations

        while not found and not eod:
            cells = []
            for j in WINNING_COMBINATIONS[i]:
                cells.append(self.cells[j])
            if is_winning_combination(cells):
                found = True
            else:
                i += 1
            eod = i >= nb_combinations

        return f"Player {cells[0].get_turns()[0][0]}" if found else ""

    def enable(self):
        for cell in self.cells:
            cell.enable()

    def disable(self, save=False):
        for cell in self.cells:
            cell.disable(save=save)

    def disable_reduced_cells(self):
        for cell in self.cells:
            if cell.is_reduced:
                cell.disable()

    def disable_entangled_cells(self, cell):
        if cell.is_entangled():
            cell.disable()
        for i in range(NB_CELLS):
            if i not in cell.selectable_cells:
                self.cells[i].disable()

    def disable_forbidden_cells(self, cell):
        self.disable_reduced_cells()
        self.disable_entangled_cells(cell)

    def restart(self):
        self.enable()
        self.players.reinit()
        for cell in self.cells:
            cell.reinit()
