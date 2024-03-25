# -*- coding: utf-8 -*-
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
SELECTABLE_CELLS_SCOPE = [
    [0, 1, 3, 4],
    [0, 1, 2, 3, 4, 5],
    [1, 2, 4, 5],
    [0, 1, 3, 4, 6, 7],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [1, 2, 4, 5, 7, 8],
    [3, 4, 6, 7],
    [3, 4, 5, 6, 7, 8],
    [4, 5, 7, 8],

]

NEIGHBOR_CELLS = [
    [1, 3, 4],
    [0, 2, 3, 4, 5],
    [1, 4, 5],
    [0, 1, 4, 6, 7],
    [0, 1, 2, 3, 5, 6, 7, 8],
    [1, 2, 4, 7, 8],
    [3, 4, 7],
    [3, 4, 5, 6, 8],
    [4, 5, 7],

]

NB_CELLS = 9

WINNING_COMBINATIONS = [
    # columns
    range(0, 3),
    range(3, 6),
    range(6, 9),

    # lines
    range(0, 9, 3),
    range(1, 9, 3),
    range(2, 9, 3),

    # diagonals
    range(0, 9, 4),
    range(2, 7, 2),
]
