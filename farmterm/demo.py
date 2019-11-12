from dataclasses import dataclass
from pprint import pprint
from typing import Any, List, Optional
import time

import blessings
import numpy as np

#: Newline
NL = "\n"
GRASS_P = [22, 28, 34, 40, 46, 70, 76]
SOIL_ORGANIC_MATTER_RANGE = np.arange(1, 100)
BRAILLE_CHARACTER_RANGE = "⠠⠔⣈⡬⣕⣫⣯"
FURROWED_STR=" ║"




def matrix_print(matrix, palette=None):
    print(NL + "# Raw print loop")
    for row in matrix:
        print(row)

    print(NL + "# pprint")
    pprint(matrix)

    print(NL + "# blessings")
    term = blessings.Terminal()
    for row in matrix:
        for c in row:
            print(term.white + term.on_green + str(c), end="")
        print(term.normal + NL)


def random_matrix(size, choices):
    # Uniform distribution matrix of choices
    return np.random.choice(choices, size=size)


def matrix_from_termcolors():
    term = blessings.Terminal()
    d = int(np.ceil(np.sqrt(term.number_of_colors)))
    colors = np.arange(term.number_of_colors)
    colors.resize((d, d))
    # __import__('IPython').embed()
    return colors


def int_range_to_max_digits(a):
    """Given an ndarray, return the character width of the decimal
    representation of the max value."""
    return len(str(max(a)))


def blessings_demo(matrix, palette=None):
    import string

    term = blessings.Terminal()
    if not palette:
        palette = {}
    print(NL + "# Colors demo")
    for row in matrix:
        for c in row:
            # print(term.on_color(c) + str(c), end='')
            # print(c)
            print(term.on_color(c) + str(c).rjust(4), end="")
        print(term.normal)


def colorspace_by_8():
    """Print out all colors in terminal in 8-wide format"""
    term = blessings.Terminal()
    colors = np.arange(term.number_of_colors)
    colors.resize((256 // 7, 7))
    print("# colorspace by 8")
    for r in colors:
        for c in r:
            print(term.on_color(c) + str(c).rjust(3), end="")
        print(term.normal)


def grass_demo():

    random_grass = np.random.choice(GRASS_P, (10, 10))
    pp_mat(random_grass, GRASS_P)


def pp_mat(matrix, palette):
    """Pretty print a matrix given a palette."""
    term = blessings.Terminal()
    for r in matrix:
        for c in r:
            # __import__("IPython").embed()
            print(term.on_color(c) + str(c).rjust(2), end="")
        print()


@dataclass
class GrassField:
    x: int
    y: int
    # FIXME: uses the number of colors, should use something like the max of either
    colors: List
    characters: List
    matrix: Optional[Any]
    term: Optional[Any]

    def __post_init__(self):
        # Create an initial random
        if not self.matrix:
            self.matrix = np.random.randint(
                len(self.colors), size=(self.x, self.y)
            )
        if not self.term:
            self.term = blessings.Terminal()

    def __repr__(self):
        """render color string to terminal"""
        s = []
        for r in self.matrix:
            for c in r:
                color = self.colors[c]
                char = self.characters[c]
                s.append(self.term.on_color(self.colors[c]) + char + char)
            s.append(NL)
        return "".join(s) + self.term.normal

    def grow(self):
        rr = np.random.randint(0, 1, size=(self.x, self.y), dtype=int)
        self.matrix += np.random.randint(2, size=(self.x, self.y))
        # mod 0-6
        # self.matrix += self.matrix < 0
        self.matrix -= (self.matrix > 6).astype(int)



def fullscreen_demo():
    print("#: fullscreen demo")
    term = blessings.Terminal()
    with term.fullscreen():
        grass = GrassField(10, 10, GRASS_P, BRAILLE_CHARACTER_RANGE, matrix=None, term=term)
        grass.grow()


        for t in range(100):
            print(term.clear())
            print(f"t{t}\t")

            print(grass.__repr__())
            time.sleep(1)
            grass.grow()
            if (grass.matrix == 6).all():
                break


def main():
    # x = np.arange(5)
    # matrix = np.matrix([x] * 5)
    # matrix_print(matrix)

    print(NL)
    # blessings_demo(matrix)
    print("# Termcolors")

    matrix = matrix_from_termcolors()
    print(matrix)
    blessings_demo(matrix)
    # colorspace_by_8()
    grass_demo()
    fullscreen_demo()


if __name__ == "__main__":
    main()
