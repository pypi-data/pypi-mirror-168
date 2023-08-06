"""
Provides an assortment of more advanced linear algebra tools to work
    with `Vector` and `Matrix` objects.
"""

from __future__ import annotations

from fractions import Fraction
from math import sqrt, acos
from typing import Iterable, Literal, overload
from functools import reduce
from operator import mul as mul_operator

from ._errors import (
    DimensionMismatchError,
    LinearDependenceError,
    RectangularMatrixError,
)
from ._matrix import Matrix
from ._vector import Vector

__all__ = (
    "cross",
    "determinant",
    "distance",
    "homogenous",
    "identity",
    "inverse",
    "join_vectors",
    "laplace_expansion",
    "limit_denominator",
    "magnitude",
    "matrix_power",
    "normalize",
    "orthogonalize",
    "rank",
    "row_reduce",
    "transpose",
    "split_vectors",
)


def angle(
    direction_a: Vector,
    direction_b: Vector,
) -> float:
    """
    Calculates the angle between two vectors in radians.

    Arguments
    - direction_a: The "starting" direction.
    - direction_b: The "ending" direction.

    Possible Errors
    - DimensionMismatchError: If `direction_a` and `direction_b` do not
        have the same length.

    Notes
    - May introduce floating point errors.
    """
    if len(direction_a) != len(direction_b):
        raise DimensionMismatchError(
            f"'a' length ({len(direction_a)}) "
            f"does not equal 'b' length ({len(direction_b)})"
        )
    return acos(
        (direction_a @ direction_b)
        / (magnitude(direction_a) * magnitude(direction_b))
    )


def cross(
    *vectors: Vector,
) -> Vector:
    """
    Calculates a vector that is orthogonal to every given vector, in the
        case of exactly two 3-dimensional inputs, this is the cross
        product.

    Arguments
    - *vectors: The collection of vectors to cross (the number of
        vectors) given must be one less than the length of each vector.

    Possible Errors
    - ValueError: If the vectors given for `vectors` are not all the
        same length _n_, or if not exactly _n_-1 vectors were given.
    """
    if len(vectors) <= 0:
        raise ValueError("exactly n-1 n-dimensional vectors must be given")
    v_len = len(vectors[0])
    for vector in vectors:
        if len(vector) != v_len:
            raise DimensionMismatchError(
                "all given vectors must have the same length"
            )
    if len(vectors) != v_len - 1:
        raise ValueError("exactly n-1 n-dimensional vectors must be given")
    matrix = join_vectors(homogenous(v_len, 1), *vectors, orientation="row")
    return Vector(
        coefficient * determinant(matrix)
        for matrix, coefficient in laplace_expansion(matrix)
    )


def determinant(
    matrix: Matrix,
) -> Fraction:
    """
    Calculates the determinant of a matrix, which represents the scaling
        factor a matrix would apply when acting as a linear
        transformation.

    Arguments
    - matrix: The matrix for which the determinant is to be calculated.

    Possible Errors
    - RectangularMatrixError: If `matrix` is not a square matrix.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise RectangularMatrixError(
            "Determinants are only defined for square "
            "matrices, this matrix has a shape of "
            f"({matrix.shape[0]},{matrix.shape[1]})"
        )
    if matrix.shape == (1, 1):
        return matrix[0, 0]
    if matrix.shape == (2, 2):
        return (matrix[0, 0] * matrix[1, 1]) - (matrix[1, 0] * matrix[0, 1])
    if matrix.shape == (3, 3):
        return (
            (matrix[0, 0] * matrix[1, 1] * matrix[2, 2])
            + (matrix[0, 1] * matrix[1, 2] * matrix[2, 0])
            + (matrix[0, 2] * matrix[1, 0] * matrix[2, 1])
            - (matrix[0, 2] * matrix[1, 1] * matrix[2, 0])
            - (matrix[0, 1] * matrix[1, 0] * matrix[2, 2])
            - (matrix[0, 0] * matrix[1, 2] * matrix[2, 1])
        )
    upper, sign = _ref(matrix)
    return reduce(mul_operator, upper.diagonal, Fraction(sign))


def distance(
    point_a: Vector,
    point_b: Vector,
) -> float:
    """
    Calculates the straight-line distance between two _n_-dimensional
        points given by vectors.

    Arguments
    - point_a: The "starting" point.
    - point_b: The "ending" point.

    Possible Errors
    - DimensionMismatchError: If `point_a` and `point_b` do not have the
        same length.

    Notes
    - May introduce floating point errors.
    """
    if len(point_a) != len(point_b):
        raise DimensionMismatchError(
            f"'a' length ({len(point_a)}) "
            f"does not equal 'b' length ({len(point_b)})"
        )
    difference = point_a - point_b
    return sqrt(difference @ difference)


@overload
def homogenous(
    shape: tuple[int, int],
    value: float | Fraction = 0,
) -> Matrix:
    ...


@overload
def homogenous(
    shape: int,
    value: float | Fraction = 0,
) -> Vector:
    ...


def homogenous(
    shape: tuple[int, int] | int,
    value: float | Fraction = 0,
) -> Vector | Matrix:
    """
    Constructor that creates a matrix or vector of a given shape which
        has all elements equal to one another.

    Arguments
    - shape: The row-column shape of the desired matrix, or length of
        the desired vector.
    - value: The value with which to fill the matrix.
        Optional, defaults to 0.
    """
    if isinstance(shape, tuple):
        return Matrix(
            (value for _ in range(shape[1])) for _ in range(shape[0])
        )
    else:  # if isinstance(shape, int):
        return Vector(value for _ in range(shape))


def identity(
    side_length: int,
) -> Matrix:
    """
    Creates and returns a square identity matrix.

    Arguments
    - side_length: The side-length of the desired matrix.

    Possible Errors
    - ValueError: If `side_length` is 0 (or less).
    """
    if side_length <= 0:
        raise ValueError("The size of an identity matrix must be at least 1")
    return Matrix(
        (1 if i == j else 0 for i in range(side_length))
        for j in range(side_length)
    )


def inverse(
    matrix: Matrix,
) -> Matrix:
    """
    Inverts a matrix with respect to matrix multiplication.

    Arguments
    - matrix: The matrix to invert.

    Possible Errors
    - RectangularMatrixError: If `matrix` is not a square matrix.
    - LinearDependenceError: If `matrix` is non-invertible.
    """
    side_len = matrix.shape[0]
    if side_len != matrix.shape[1]:
        raise RectangularMatrixError(
            "inversions are only defined for square "
            "matrices, this matrix has a shape of "
            f"({matrix.shape[0]},{matrix.shape[1]})"
        )
    reduction = row_reduce(matrix | identity(side_len))
    inversion = reduction[:, side_len:]
    for i in reduction.diagonal:
        if i != Fraction(1):
            raise LinearDependenceError(
                "cannot invert linearly dependent matrices"
            )
    return inversion


def join_vectors(
    *vectors: Vector,
    orientation: Literal["col", "row"] = "col",
) -> Matrix:
    """
    Concatenates _m_ vectors of dimension _n_ into either an _m_ by _n_
        matrix, or an _n_ by _m_ matrix.

    Arguments
    - *vectors: The vectors to join.
    - orientation: Whether to interpret the given vectors as columns, or
        as rows of the desired matrix.
        Optional, defaults to 'col'.

    Possible Errors
    - ValueError: If no vectors were given.
    - DimensionMismatchError: If not all of the given vectors have the
        same length.
    """
    if len(vectors) <= 0:
        raise ValueError("at least one vector must be given")
    v_len = len(vectors[0])
    for vector in vectors:
        if len(vector) != v_len:
            raise DimensionMismatchError(
                "all vectors must have the same length to be "
                "joined into a matrix"
            )
    if orientation == "col":
        return Matrix(row for row in zip(*vectors))
    else:  # if orientation == "row":
        return Matrix(vectors)


def laplace_expansion(
    matrix: Matrix,
) -> Iterable[tuple[Matrix, Fraction]]:
    """
    Lazily yields the cofactor expansion of a matrix along its first row
        as a matrix-coefficient tuple.

    Arguments
    - matrix: The matrix to expand.

    Possible Errors
    - RectangularMatrixError: If `matrix` is not a square matrix.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise RectangularMatrixError(
            "Laplace expansions are only defined for square "
            "matrices, this matrix has a shape of "
            f"({matrix.shape[0]},{matrix.shape[1]})"
        )
    if matrix.shape[0] < 2:
        raise ValueError(
            "matrices must not be smaller than (2,2) for Laplace expansion"
        )
    for i in range(matrix.shape[1]):
        yield (
            Matrix(
                (item for c, item in enumerate(row) if c != i)
                for r, row in enumerate(matrix)
                if r != 0
            ),
            (1 if i % 2 == 0 else -1) * matrix[0, i],
        )


@overload
def limit_denominator(
    arg: Vector,
    max_denominator: int,
) -> Vector:
    ...


@overload
def limit_denominator(
    arg: Matrix,
    max_denominator: int,
) -> Matrix:
    ...


def limit_denominator(
    arg: Vector | Matrix,
    max_denominator: int,
) -> Vector | Matrix:
    """
    Creates a new instance of the argument with all fraction
        denominators set to some maximum amount.

    Arguments
    - arg: The matrix or vector to operate on.
    - max_denominator: The highest possible denominator (actual may be
        lower).

    Possible Errors
    - ZeroDivisionError: If max_denominator is 0.
    """

    if max_denominator == 0:
        raise ZeroDivisionError(
            "maximum denominator must be a nonzero positive integer"
        )
    if isinstance(arg, Matrix):
        return Matrix(
            (item.limit_denominator(max_denominator) for item in row)
            for row in arg
        )
    else:  # if isinstance(arg, Vector):
        return Vector(item.limit_denominator(max_denominator) for item in arg)


def magnitude(
    vector: Vector,
) -> float:
    """
    Calculates the magnitude (length) of a given vector.

    Arguments
    - vector: The vector for which the magnitude must be calculated.

    Notes
    - May introduce floating point errors.
    """
    return sqrt(sum((n * n for n in vector)))


def matrix_power(
    matrix: Matrix,
    power: int,
) -> Matrix:
    """
    Calculates the given integer power of a matrix by repeated matrix
        multiplication.

    Arguments
    - matrix: The matrix to raise to the given power.
    - power: The power to raise the given matrix to.

    Possible Errors
    - RectangularMatrixError: If `matrix` is not a square matrix.
    """
    side_len = matrix.shape[0]
    if not side_len == matrix.shape[1]:
        raise RectangularMatrixError(
            "only square matrices may be raised to a power"
        )
    multi = None
    if power < 0:
        multi = inverse(matrix)
        power = -power
    else:
        multi = matrix
    operand = identity(side_len)
    for _ in range(power):
        operand @= multi
    return operand


def normalize(
    vector: Vector,
) -> Vector:
    """
    Calculates an approximately normal vector.

    Arguments
    - vector: The vector to normalize.

    Possible Errors
    - ZeroDivisionError: If the magnitude of the given vector is 0.

    Notes
    - An exact normal cannot be calculated since normalization involves
        scaling by a possibly irrational factor. This may introduce
        floating point errors.
    """
    mag = magnitude(vector)
    if mag == 0:
        raise ZeroDivisionError(
            "vectors with magnitude 0 cannot be normalized"
        )
    else:
        return Vector(n / mag for n in vector)


def orthogonalize(
    *vectors: Vector,
) -> list[Vector]:
    """
    Using the Gram-Schmidt process, creates an orthogonal basis from a
        set of vectors.

    Arguments
    - *vectors: The set of vectors to use as a non-orthogonal basis.

    Possible Errors
    - ValueError: If not all given vectors have the same length, or
        if not exactly *n* vectors are given, where *n* represents the
        length of each vector.
    - LinearDependenceError: If the given vectors cannot form a linearly
        independent basis.

    Notes
    - The returned vectors are not normalized, they must be manually
        normalized if an orthonormal basis is sought.
    """
    if len(vectors) <= 0:
        raise ValueError("exactly n n-dimensional vectors must be given")
    v_len = len(vectors[0])
    for vector in vectors:
        if len(vector) != v_len:
            raise DimensionMismatchError(
                "all given vectors must have the same length"
            )
    if len(vectors) != v_len:
        raise ValueError("exactly n n-dimensional vectors must be given")
    u_vectors: list[Vector] = []
    try:
        for k in range(len(vectors)):
            u_vectors.append(vectors[k])
            u_vectors[k] -= sum(
                (
                    (
                        u_vectors[i]
                        * (vectors[k] @ u_vectors[i])
                        / (u_vectors[i] @ u_vectors[i])
                    )
                    for i in range(k)
                ),
                start=homogenous(v_len, 0),
            )
    except ZeroDivisionError:
        raise LinearDependenceError(
            "cannot orthogonalize linearly dependent vectors"
        )

    return u_vectors


def rank(
    matrix: Matrix,
) -> int:
    """
    Calculates the rank of a given matrix.

    Arguments
    - matrix: The matrix the rank is to be calculated from.
    """
    matrix_ref = row_reduce(matrix, "ref")
    rank_count = 0
    for i in range(min(matrix_ref.shape)):
        if matrix_ref[i, i] == 0:
            break
        else:
            rank_count += 1
    return rank_count


def row_reduce(
    matrix: Matrix,
    form: Literal["rref", "ref"] = "rref",
) -> Matrix:
    """
    Computes a row-echelon or reduced row-echelon form matrix by row
        reduction.

    Arguments
    - matrix: The matrix to row-reduce.
    - form: Whether to compute the reduced row-echelon form by
        Gauss-Jordan elimination, or compute a non-reduced row-echelon
        form by simple Gaussian elimination.
        Optional, defaults to 'rref'.
    """
    if form == "rref":
        return _rref(matrix)
    else:  # if form == "ref":
        return _ref(matrix)[0]


def split_vectors(
    matrix: Matrix,
    orientation: Literal["col", "row"] = "col",
) -> Iterable[Vector]:
    """
    Lazily gets each row or column from a matrix as a vector.

    Arguments
    - matrix: The matrix to separate into vectors.
    - orientation: Whether to interpret the given matrix as a collection
        of columns, or a list of rows.
        Optional, defaults to 'col'.
    """
    if orientation == "col":
        return (Vector(col) for col in zip(*iter(matrix)))
    else:  # if orientation == "row":
        return (Vector(col) for col in matrix)


def transpose(
    matrix: Matrix,
) -> Matrix:
    """
    Calculate the transpose of a given matrix.

    Arguments
    - matrix: The matrix to transpose.
    """
    return Matrix(
        (matrix[i, j] for i in range(matrix.shape[0]))
        for j in range(matrix.shape[1])
    )


# PRIVATE/PROTECTED METHODS


def _ref(
    matrix: Matrix,
) -> tuple[Matrix, int]:
    """
    Using Gaussian elimination, calculates and returns the row-echelon
        form of a matrix.

    Arguments
    - matrix: The matrix to row-reduce.
    """
    list_mat = matrix.elements
    lm_shape = matrix.shape
    row_count = lm_shape[0]
    col_count = lm_shape[1]
    pivot_row = 0
    pivot_col = 0
    det_sign = 1

    while pivot_row < row_count and pivot_col < col_count:
        max_row = max(
            (
                (abs(list_mat[i][pivot_col]), i)
                for i in range(pivot_row, row_count)
            ),
            key=lambda x: x[0],
        )[1]
        if list_mat[max_row][pivot_col] == Fraction(0):
            pivot_col += 1
        else:
            if max_row != pivot_row:
                list_mat[pivot_row], list_mat[max_row] = (
                    list_mat[max_row],
                    list_mat[pivot_row],
                )
                det_sign = -det_sign
            for row in range(pivot_row + 1, row_count):
                factor = (
                    list_mat[row][pivot_col] / list_mat[pivot_row][pivot_col]
                )
                list_mat[row][pivot_col] = Fraction(0)
                for col in range(pivot_col + 1, col_count):
                    list_mat[row][col] -= list_mat[pivot_row][col] * factor
            pivot_row += 1
            pivot_col += 1
    return Matrix(list_mat), det_sign


def _rref(
    matrix: Matrix,
) -> Matrix:
    """
    Using Gauss-Jordan elimination, calculates and returns the
        reduced row-echelon form of a matrix.

    Arguments
    - matrix: The matrix to row-reduce.
    """
    list_mat = matrix.elements
    lm_shape = matrix.shape
    lead = 0
    row_count = lm_shape[0]
    col_count = lm_shape[1]
    for row in range(row_count):
        if col_count <= lead:
            return Matrix(list_mat)
        i = row
        while list_mat[i][lead] == Fraction(0):
            i += 1
            if row_count == i:
                i = row
                lead += 1
                if col_count == lead:
                    return Matrix(list_mat)
        if i != row:
            list_mat[i], list_mat[row] = list_mat[row], list_mat[i]
        lead_val = list_mat[row][lead]
        for col in range(lm_shape[1]):
            list_mat[row][col] = list_mat[row][col] / lead_val
        for i in range(row_count):
            if i != row:
                lead_val = list_mat[i][lead]
                for col in range(lm_shape[1]):
                    list_mat[i][col] = list_mat[i][col] - (
                        lead_val * list_mat[row][col]
                    )
        lead += 1
    return Matrix(list_mat)
