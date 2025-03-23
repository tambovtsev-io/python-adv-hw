from numbers import Number
from pathlib import Path
from typing import List

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from mixins import SaveMixin, ToStringMixin


class MatrixNumpy(
    SaveMixin,
    ToStringMixin,
    NDArrayOperatorsMixin,
):
    _HANDLED_TYPES = (np.ndarray, Number)

    def __init__(self, data: List[List[float]]):
        self._data = np.array(data)
        self.rows = len(data)
        self.cols = len(data[0]) if isinstance(data, list) else 0

    @property
    def data(self):
        return self._data

    @property
    def shape(self):
        return self.rows, self.cols

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Adopted example from docs: https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html"""
        out = kwargs.get("out", ())
        for x in inputs + out:
            # Only support operations with instances of
            # _HANDLED_TYPES. Use ArrayLike instead of type(self)
            # for isinstance to allow subclasses that don't
            # override __array_ufunc__ to handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (MatrixNumpy,)):
                return NotImplemented
        # Defer to the implementation of the ufunc
        # on unwrapped values.
        inputs = tuple(x._data if isinstance(x, MatrixNumpy) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(
                x._data if isinstance(x, MatrixNumpy) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)


def task_2():
    np.random.seed(0)

    A = MatrixNumpy(np.random.randint(0, 10, (10, 10)).tolist())
    B = MatrixNumpy(np.random.randint(0, 10, (10, 10)).tolist())

    artifacts_dir = Path("artifacts") / "task2"
    A.save_to_file(artifacts_dir / "A.txt")
    B.save_to_file(artifacts_dir / "B.txt")

    # Operations with numbers
    (A + 10).save_to_file(artifacts_dir / "matrix+num.txt")
    (A * 10).save_to_file(artifacts_dir / "matrix*num.txt")

    # Operations with matrices
    (A + B).save_to_file(artifacts_dir / "matrix+matrix.txt")
    (A * B).save_to_file(artifacts_dir / "matrix*matrix.txt")
    (A @ B).save_to_file(artifacts_dir / "matrix@matrix.txt")


if __name__ == "__main__":
    task_2()
