"""
Definition of the different VarArrays and some better explained nice to have functions
"""
# python imports
from typing import Tuple
# third-party imports
import numpy as np
# local imports
from manim_meshes.exceptions import FaultyVarArrayException
from manim_meshes.helpers import is_twice_nested_iterable


class VarArray(list):
    """
    Class for VarArray object
    A VarArray is a list of np.ndarray's where the size of the arrays can differ
    """
    def __init__(self, obj, rolling, min_lens: Tuple[int, int] = (1, 3)):
        """initialize VarArray """
        if not is_twice_nested_iterable(obj=obj, min_lens=min_lens):
            raise FaultyVarArrayException("The given object is no VarArray or no twice nested iterable.")
        # own params
        self.rolling = rolling
        # call init of base list and convert everything to np.array
        super().__init__([np.array(x, dtype=int) for x in obj])

    def __getitem__(self, key) -> np.ndarray:
        return list.__getitem__(self, key)

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            # other is a np.ndarray
            if len(other.shape) == 2:
                # two-dimensional means we add a list of one dimensional arrays to self
                self.append(v for v in other)
            elif len(other.shape) == 1:
                # one-dimensional means we can append other directly
                self.append(other)
            else:
                raise FaultyVarArrayException(f'other has not the correct shape {other}')
            return self
        if isinstance(other, (list, tuple)):
            # other is an iterable
            if all(isinstance(v, np.ndarray) for v in other):
                # case one iterable
                self.append(v for v in other)
            elif all(isinstance(val, int) for val in other):
                # case one iterable with plain values
                try:
                    self.append(np.array(other))
                except (np.VisibleDeprecationWarning, TypeError, ValueError) as e:
                    raise FaultyVarArrayException("other can not be cast to np.ndarray directly") from e
            elif all(isinstance(v, (list, tuple)) for v in other):
                # case one iterable with iterables inside
                try:
                    new_vals = [np.array(v) for v in other]
                    self.append(v for v in new_vals)
                except (np.VisibleDeprecationWarning, TypeError, ValueError) as e:
                    raise FaultyVarArrayException("not all values in other can be cast to np.ndarray") from e
            else:
                raise FaultyVarArrayException("Type of nested values not recognized")
            return self
        raise FaultyVarArrayException("Other is not iterable")
