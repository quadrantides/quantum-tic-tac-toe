# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
NB_PLAYERS = 2

NAMES = ["X", "O"]
ACTIVES = [True, False]
TURN_DEFAULT_INDEX = [1, 2]


class Player(object):
    def __init__(self, name, active=False, turn_default_index=1):
        self.name = ""
        self.default = dict(
            active=active,
            turn_default_index=turn_default_index,
        )
        self.name = name
        self.active = False
        self.turn_index = 0
        self.turn_step = 0
        self.init()

    def init(self):
        self.turn_index = self.default["turn_default_index"]
        self.active = self.default["active"]
        self.init_turn_step()

    def init_turn_step(self):
        self.turn_step = 0

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def increase_turn_step(self):
        self.turn_step += 1

    def next_turn_index(self):
        self.turn_index += 2

    def get_turn_index(self):
        return self.turn_index

    def get_metrics(self):
        return [
            "Player metrics",
            f"active : {self.active}, turn : {self.name}{self.turn_index}, turn step : {self.turn_step}",
        ]

    def is_first_turn(self):
        return self.turn_step == 1

    def is_second_turn(self):
        return self.turn_step == 2


class Players(object):
    def __init__(self):
        self.players = []
        self.init()

    def init(self):
        for i in range(NB_PLAYERS):
            self.players.append(
                Player(
                    NAMES[i],
                    active=ACTIVES[i],
                    turn_default_index=TURN_DEFAULT_INDEX[i],
                )
            )

    def reinit(self):
        for player in self.players:
            player.init()

    def get_active_player(self):
        return self.players[0] if self.players[0].active else self.players[1]

    def get_inactive_player(self):
        return self.players[0] if not self.players[0].active else self.players[1]

    def next_player(self):
        active_player = self.get_active_player()
        inactive_player = self.get_inactive_player()

        old_active_player = active_player
        old_active_player.set_inactive()
        old_active_player.init_turn_step()

        new_active_player = inactive_player
        new_active_player.set_active()
        new_active_player.next_turn_index()

    def increase_active_player_turn_step(self):
        active_player = self.get_active_player()
        active_player.increase_turn_step()

    def get_turn(self):
        player = self.get_active_player()
        return f"{player.name}{player.turn_index}"

    def get_player(self, name):
        eod = False
        found = 0
        i = 0

        while not found and not eod:
            player = self.players[i]
            if player.name == name:
                found = True
            else:
                i += 1
            if i == NB_PLAYERS:
                eod = True
        if not found:
            player = None
        return player

    def is_o_active_player(self):
        player = self.get_active_player()
        return player.name == "O"

    def get_active_player_metrics(self):
        player = self.get_active_player()
        return player.get_metrics()


if __name__ == '__main__':

    p = Players()
    m = p.get_active_player_metrics()
    print(m)
