import operator
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from mixins import MatrixHashMixin, SaveMixin, ToStringMixin


class Matrix(
    MatrixHashMixin,
    SaveMixin,
    ToStringMixin,
):
    __hash__ = MatrixHashMixin.__hash__
    matmul_cache: Dict[Tuple[int, int], "Matrix"] = dict()

    def __init__(self, data: List[List[float]]):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if isinstance(data, list) else 0

    def element_wise_operation(self, other: "Matrix", operation: Callable) -> "Matrix":
        """
        Method for element-wise operations
        other: Another matrix
        operation: Operation to perform (e.g., operator.add, operator.mul)

        return: New matrix with results
        """
        if not isinstance(other, Matrix):
            raise ValueError("Can only operate with Matrix objects")
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise ValueError(
                "Matrices must have same dimensions for element-wise operations"
            )

        result = [
            [operation(self.data[i][j], other.data[i][j]) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __add__(self, other: "Matrix") -> "Matrix":
        return self.element_wise_operation(other, operator.add)

    def __mul__(self, other: "Matrix") -> "Matrix":
        return self.element_wise_operation(other, operator.mul)

    @classmethod
    def _matmul_matrices(cls, m1: "Matrix", m2: "Matrix") -> "Matrix":
        result = [
            [
                sum(m1.data[i][k] * m2.data[k][j] for k in range(m1.cols))
                for j in range(m2.cols)
            ]
            for i in range(m1.rows)
        ]
        return Matrix(result)

    def __matmul__(self, other) -> "Matrix":
        if not isinstance(other, Matrix):
            raise ValueError("Can only matrix multiply Matrix objects")
        if self.cols != other.rows:
            raise ValueError("Invalid dimensions for matrix multiplication")

        # Return cached result if available
        cache_key = (hash(self), hash(other))
        if cache_key in Matrix.matmul_cache:
            return Matrix.matmul_cache[cache_key]

        # Calc and add to cache otherwise
        result = self._matmul_matrices(self, other)
        Matrix.matmul_cache[cache_key] = result
        return result

    @classmethod
    def clear_cache(cls):
        cls.matmul_cache.clear()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            all(row) for row in self.element_wise_operation(other, operator.eq).data
        )


def task_1():
    import numpy as np

    np.random.seed(0)

    A = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    B = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    addition = A + B
    element_mult = A * B
    matrix_mult = A @ B

    artifacts_dir = Path("artifacts") / "task1"
    addition.save_to_file(artifacts_dir / "matrix+.txt")
    element_mult.save_to_file(artifacts_dir / "matrix*.txt")
    matrix_mult.save_to_file(artifacts_dir / "matrix@.txt")


def task_3_find_collision():
    # Create matrices with same hash but different values
    # Using matrices where product of elements is the same
    A = Matrix([[2, 3], [2, 2]])  # Product = 24
    B = Matrix([[1, 2], [3, 4]])

    C = Matrix([[4, 3], [1, 2]])  # Product = 24 (same as A)
    D = Matrix([[1, 2], [3, 4]])  # Same as B

    AB = A @ B
    CD_cached = C @ D
    Matrix.clear_cache()
    CD = C @ D

    # Assert task conditions: (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D)
    assert hash(A) == hash(C), "Failed hash(A) == hash(C)"
    assert A != C, "Failed A != C"
    assert B == D, "Failed B == D"
    assert (AB).data != (CD).data, "Failed A @ B != C @ D"

    # Save all matrices
    artifacts_dir = Path("artifacts") / "task3"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    A.save_to_file(artifacts_dir / "A.txt")
    B.save_to_file(artifacts_dir / "B.txt")
    C.save_to_file(artifacts_dir / "C.txt")
    D.save_to_file(artifacts_dir / "D.txt")
    AB.save_to_file(artifacts_dir / "AB.txt")
    CD.save_to_file(artifacts_dir / "CD_true.txt")
    CD_cached.save_to_file(artifacts_dir / "CD_cached.txt")

    # Save hash
    hash_file = artifacts_dir / "hash.txt"
    hash_file.write_text(f"{hash(A @ B)}\n{hash(C @ D)}")


if __name__ == "__main__":
    task_1()
    task_3_find_collision()
