from __future__ import annotations
from linalg.field import Field, FieldScalar


class Matrix:
    def __init__(self, f: Field, array: list[list[FieldScalar]]) -> None:
        assert len(array) > 0, "Cannot initialize an empty matrix."
        assert all(len(row) > 0 for row in array), "Cannot initialize an empty row."

        self.field = f
        for row in array:
            for elt in row:
                assert isinstance(
                    elt, self.field.scalars
                ), f"{elt} of type {type(elt)} must be of type {self.field.scalars}."

        self.array = array
        self.shape = (len(array), len(array[0]))

    def __eq__(self, other) -> bool:
        assert isinstance(other, Matrix), TypeError(
            f"Cannot compare {type(self)} with {type(other)}."
        )
        return self.array == other.array

    def __str__(self) -> str:
        return "\n".join(["\t".join(map(str, row)) for row in self.array])

    def __add__(self, other) -> Matrix:
        assert isinstance(other, Matrix), TypeError(
            f"Cannot add {type(self)} to {type(other)}."
        )
        assert self._is_like(other), ValueError(
            f"Cannot add shape {self.shape} to shape {other.shape}."
        )

        result = []
        for row1, row2 in zip(self.array, other.array):
            newrow = []
            for a, b in zip(row1, row2):
                newrow.append(a + b)
            result.append(newrow)

        return Matrix(self.field, result)

    def __mul__(self, other) -> Matrix:
        assert isinstance(other, Matrix), TypeError(
            f"Cannot multiply {type(self)} and {type(other)}."
        )
        assert self.shape[1] == other.shape[0], ValueError(
            f"Cannot multiply shape {self.shape} and {other.shape}."
        )

        result = zeros(self.shape[0], other.shape[1], self.field)

        for rowidx in range(self.shape[0]):
            for colidx in range(other.shape[1]):
                for elt in range(self.shape[1]):
                    result.array[rowidx][colidx] += (
                        self.array[rowidx][elt] * other.array[elt][colidx]
                    )
        return result

    def transpose(self) -> Matrix:
        new_array = [
            [self.array[j][i] for j in range(len(self.array))]
            for i in range(len(self.array[0]))
        ]
        return Matrix(self.field, new_array)

    def _copy(self) -> Matrix:
        return Matrix(self.field, self.array[:])

    def _is_square(self) -> bool:
        return self.shape[0] == self.shape[1]

    def _is_like(self, other) -> bool:
        return self.shape == other.shape

    def _flip(self) -> Matrix:
        new_array = self.array[:]
        for row in new_array:
            row = row[::-1]
        return Matrix(self.field, new_array[::-1])

    def trace(self) -> FieldScalar:
        assert self._is_square(), "Matrix must be square."
        result = self.field.getZero()
        for i in range(self.shape[0]):
            result += self.array[i][i]
        return result

    def REF(self, row_start=0, mimic=None) -> list[Matrix]:
        """Puts the given Matrix in row echelon form."""
        zero = self.field.getZero()

        current_row_index = row_start
        local = self._copy()
        rowsize = len(local.array)

        if mimic:
            assert isinstance(mimic, Matrix), TypeError("Mimic must be a Matrix")
            assert self._is_like(mimic), ValueError(
                "Mimic must have same shape as matrix argument."
            )

        while current_row_index < local.shape[0]:
            current_row = local.array[current_row_index]
            if current_row != [zero for _ in range(len(current_row))]:

                # Current row is not zero. Find first non-zero entry of current row.
                k = min([current_row.index(a) for a in current_row if a != zero])
                pivot = current_row[k]
                pivot_inverse = ~pivot

                # Normalize pivot.
                diag = diagonal(
                    local.field,
                    pivot_inverse,
                    rowsize,
                    current_row_index,
                )

                mimic = diag * mimic if mimic else None
                local = diag * local

                for i in range(current_row_index + 1, local.shape[0]):
                    # Make sure that A[i][k] = 0 for any other larger i through row operations.

                    t_matrix = translation(
                        local.field,
                        -local.array[i][k],
                        rowsize,
                        i,
                        current_row_index,
                    )

                    mimic = t_matrix * mimic if mimic else None
                    local = t_matrix * local

            current_row_index += 1

        if mimic:
            return [Matrix(local.field, local.array), Matrix(local.field, mimic.array)]

        return [Matrix(local.field, sorted(local.array, reverse=True))]

    def invert(self) -> Matrix | None:
        """Computes the inverse of the given Matrix if possible. Returns
        None if the matrix is not invertible."""

        assert self._is_square(), ValueError("Cannot invert a non-square matrix.")

        size = self.shape[0]
        id = identity(size, self.field)
        local = self._copy()

        iter1 = local.REF(mimic=id)
        iter1 = [iter1[0]._flip(), iter1[1]._flip()]

        iter2 = iter1[0].REF(mimic=iter1[1])

        if iter2[0]._flip() == id:
            return iter2[1]._flip()
        else:
            return None

    def zeros_like(self) -> Matrix:
        """Returns a matrix of zeros of the same shape as the given matrix."""
        result = []
        for row in self.array:
            result.append([self.field.getZero() for _ in row])
        return Matrix(self.field, result)

    def RREF(self) -> Matrix:
        """Computes the reduced row echelon form of a Matrix."""

        local = self._copy().REF()[0]
        rowsize, colsize = local.shape

        for col_idx in range(colsize):
            pivot_idxs = [
                row_idx
                for row_idx in range(rowsize)
                if local.array[row_idx][col_idx] == local.field.getOne()
            ]

            pivot_idx = max(pivot_idxs) if pivot_idxs else 0

            for row_idx in range(pivot_idx):
                # Subtract row of pivot_idx to row of row_idx.
                t_matrix = translation(
                    local.field,
                    -local.array[row_idx][col_idx],
                    rowsize,
                    row_idx,
                    pivot_idx,
                )
                local = (t_matrix * local) if local.array[row_idx][col_idx] else local
        return local


def zeros(rows: int, cols: int, f: Field) -> Matrix:
    result = []
    for _ in range(rows):
        result.append([f.getZero() for _ in range(cols)])
    return Matrix(f, result)


def identity(size, field: Field) -> Matrix:
    """Returns the identity matrix over field of the given size."""
    result = []
    for i in range(size):
        row = []
        for j in range(size):
            elem = field.getZero() if i != j else field.getOne()
            row.append(elem)
        result.append(row)
    return Matrix(field, result)


def translation(f: Field, r: FieldScalar, size: int, i: int, j: int) -> Matrix:
    """Returns a square Matrix over Field of given size with
    ones in diagonal and r in off diagonal entry (i, j)

    Left multiplication by this matrix adds r times row j to row i.
    """

    id = identity(size, f)
    e = id.zeros_like()
    e.array[i][j] = r
    return id + e


def diagonal(f: Field, u: FieldScalar, size: int, i: int) -> Matrix:
    """Returns a square Matrix over Field of given size with
    u in position (i, i) and ones in other diagonal entries.

    Left multiplication by this matrix divides row i by u.
    """

    id = identity(size, f)
    e = id.zeros_like()
    e.array[i][i] = u - f.getOne()
    return id + e


def permutation(size: int, i: int, j: int, field: Field) -> Matrix:
    """Returns a square permutation Matrix over field of given size
    Left multiplication by this matrix interchanges row i with row j.
    """

    result = identity(size, field)
    result.array[i][i], result.array[i][j] = result.array[i][j], result.array[i][i]
    result.array[j][j], result.array[j][i] = result.array[j][i], result.array[j][j]
    return result
