import random as rnd
import math
import random


class Individual:
    def __init__(self, steiner_v, terminal_v, neighbour_v):
        an_individual = steiner_v + terminal_v
        self.steiner_v = steiner_v
        self.an_individual = an_individual
        self.neighbour_v = neighbour_v

    fitness = 0
