import random
from typing import Optional, Union
import numpy as np

from miua2024b.source.util import default, native, as_tuple

_default_color_names = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']


def random_colors(seed: int=0):
    """
    generator for random colors
    """
    rnd = random.Random(seed)
    while True:
        yield tuple(rnd.randint(32, 200) for _ in range(3))

def default_color(index: int) -> tuple:
    """
    returns a default color for the given index, after the last entry colors are generated randomly (with the same seed)
    """
    global _default_color_names
    assert index >= 0

    if index < len(_default_color_names):
        return to_color(_default_color_names[index])
    else:
        draw = index + 1 - len(_default_color_names)
        gen = random_colors()
        while True:
            c = next(gen)
            draw -= 1
            if draw <= 0:
                break
        return tuple(c)


def _name_to_color(name: str):
    from matplotlib import colors
    return colors.to_rgb(name)

def to_color(v: Union[int, tuple, list, str]):
    """
    returns a uint rgb value for a label int, rgb tuple or color name
    """
    if isinstance(v, str):
        v = _name_to_color(v)
    elif np.isscalar(v):
        if isinstance(v, int):
            return default_color(v)
        v = (v,) * 3
    return tuple_to_color(v)


def tuple_to_color(v: tuple):
    v = as_tuple(v)
    n = len(v)
    if n != 3:
        raise RuntimeError("Color tuples need to be of length 3 (found: {})".format(n))
    if any(not isinstance(c, int) for c in v):
        v = np.multiply(np.clip(v, a_min=0, a_max=1.0), 255).astype(int)
    else:
        v = np.clip(v, a_min=0, a_max=255).astype(int)
    return native(v)


def default_palette(size: Optional[int]):
    """
    returns an default arbitrary length color palette, after the last entry colors are generated randomly (with the same seed)
    """
    global _default_color_names
    size = default(size, len(_default_color_names))
    return list(default_color(i) for i in range(size))