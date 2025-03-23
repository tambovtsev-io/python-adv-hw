from functools import reduce
from pathlib import Path


class MatrixHashMixin:
    def __hash__(self) -> int:
        elem_product = reduce(
            lambda x, y: x * y, [x for row in self.data for x in row], 1
        )
        return elem_product


class SaveMixin:
    def save_to_file(self, fpath: Path):
        fpath.parent.mkdir(parents=True, exist_ok=True)  # Create dir
        fpath.write_text(str(self))


class ToStringMixin:
    def __str__(self) -> str:
        return "\n".join([" ".join(map(str, row)) for row in self.data])
