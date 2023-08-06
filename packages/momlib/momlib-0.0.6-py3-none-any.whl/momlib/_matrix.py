"""
Implements the `Matrix` class (see `help(Matrix)`).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import chain
from operator import (
    mul as mul_operator,
    truediv as truediv_operator,
    add as add_operator,
    sub as sub_operator,
)
from typing import (
    Any,
    Callable,
    Iterable,
    Final,
    Iterator,
    overload,
)
from collections.abc import (
    Hashable as HashableABC,
    Sequence as SequenceABC,
)

from ._errors import DimensionMismatchError

__all__ = ("Matrix",)


class Matrix(
    HashableABC,
    SequenceABC[tuple[Fraction, ...]],
):
    """
    Expresses the mathematical notion of a rational-valued matrix in
        native Python datastructures and datatypes while providing an
        assortment of tools to perform basic matrix manipulations.

    `Matrix` objects are considered non-mutable, which means that for
        the life of an object it cannot be meaningfully modified[^1].
        Matrices are, therefore, hashable (using
        `hash(matrix_instance)`).

    [^1]: If you need to modify a `Matrix`, look into the
        `matrix_instance.elements` property.
    """

    __slots__ = (
        "_data",
        "_shape",
        "_hash",
    )

    def __init__(
        self,
        initializer: Iterable[Iterable[float | Fraction]],
    ) -> None:
        """
        Initializes a new instance of the `Matrix` class.

        Arguments
        - initializer: A 2D iterable that will be used to construct the
            matrix.

        Possible Errors
        - ValueError: If the initializer has no elements, or if the
            initializer is jagged (not rectangular).
        """
        # Capture the data - necessary because the initializer could be
        # mutable, or a generator.
        data = tuple(
            tuple(Fraction(item) for item in row) for row in initializer
        )
        # Check the data shape
        if len(data) <= 0 or len(data[0]) <= 0:
            raise ValueError("matrices must have at least one element")
        num_of_cols = len(data[0])
        for row in data:
            if len(row) != num_of_cols:
                raise ValueError("matrices must be rectangular (not jagged)")
        # Set instance variables
        self._data: Final[tuple[tuple[Fraction, ...], ...]] = data
        self._shape: Final[tuple[int, int]] = (len(data), num_of_cols)
        self._hash: int | None = None

    def __len__(
        self,
    ) -> int:
        """
        Returns the total number of elements in this matrix.
        """
        return self._shape[0] * self._shape[1]

    @overload
    def __getitem__(
        self,
        key: tuple[int, int],
    ) -> Fraction:
        ...

    @overload
    def __getitem__(
        self,
        key: tuple[slice, int] | tuple[int, slice] | tuple[slice, slice],
    ) -> Matrix:
        ...

    def __getitem__(
        self,
        key: tuple[int | slice, int | slice],
    ) -> Fraction | Matrix:
        """
        Returns the items at specified coordinates in this matrix.

        Arguments
        - key: The 0-indexed row-column coordinates of the desired
            elements.

        Possible Errors
        - IndexError: If the slice would create a matrix with zero
            elements, or if an integer index is out of bounds.
        """
        key_r = key[0]
        key_c = key[1]
        try:
            if isinstance(key_r, int) and isinstance(key_c, int):
                return self._data[key_r][key_c]
            else:
                if isinstance(key_r, int):
                    key_r = (key_r, key_r + 1)
                else:
                    key_r = key_r.indices(self._shape[0])

                if isinstance(key_c, int):
                    key_c = (key_c, key_c + 1)
                else:
                    key_c = key_c.indices(self._shape[1])

                return Matrix(
                    (self._data[r][c] for c in range(*key_c))
                    for r in range(*key_r)
                )

        except IndexError:
            raise IndexError(
                f"index out of bounds, expected index in "
                f"([0, {self._shape[0]}), [0, {self._shape[0]})) but "
                f"received ({key[0]}, {key[1]})"
            )

    def __iter__(
        self,
    ) -> Iterator[tuple[Fraction, ...]]:
        """
        Returns an iterator over the rows of this matrix.
        """
        return self._data.__iter__()

    def __str__(
        self,
    ) -> str:
        """
        Returns a "pretty" string representation of this matrix.
        """
        return self._string_format(
            10,
            10,
            lambda f: (
                "%.3g" % (f.numerator if f.denominator == 1 else float(f))
            ),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Returns a reproduction string representation of this matrix.

        Notes
        - Assuming all relevant libraries have been imported, the
            reproduction string can be run as valid Python to create
            an exact copy of this matrix.
        """
        obj_name = self.__class__.__name__
        initializer = "[\n        [{}],\n    ]".format(
            "],\n        [".join(
                ", ".join(repr(item) for item in row) for row in self._data
            )
        )
        return f"{obj_name}(\n    initializer={initializer},\n)"

    def __matmul__(
        self,
        other: Matrix,
    ) -> Matrix:
        """
        Returns the matrix product of this and another
            matrix.

        Arguments
        - other: The right-hand-side operand to matrix multiplication.

        Possible Errors
        - DimensionMismatchError: If the column count of `self` does not
            match the row count of `other`.
        """
        if not isinstance(other, Matrix):  # type: ignore
            return NotImplemented
        inner_dim = self._shape[1]
        if inner_dim != other._shape[0]:
            raise DimensionMismatchError(
                f"left side columns ({self._shape[1]}) "
                f"do not equal right side rows ({other._shape[0]}), "
                "did you mean to find the Hadamard (element-wise) product "
                "instead? ('*' operator)"
            )
        return Matrix(
            (
                sum(
                    (
                        self._data[row][i] * other._data[i][col]
                        for i in range(inner_dim)
                    )
                )
                for col in range(other._shape[1])
            )
            for row in range(self._shape[0])
        )

    def __mul__(
        self,
        other: Matrix | float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise product of this matrix and either
            another matrix or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.

        Notes
        - To calculate the matrix product of two matrices, use the
            `__matmul__` (at-sign) operator.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, mul_operator)

    def __rmul__(
        self,
        other: float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise product of this matrix and either
            another matrix or a single number (if this matrix is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.

        Notes
        - To calculate the matrix product of two matrices, use the
            `__matmul__` (at-sign) operator.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, mul_operator)

    def __truediv__(
        self,
        other: Matrix | float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise quotient of this matrix and either
            another matrix or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        - ZeroDivisionError: If `other` is zero, or is a matrix that
            contains a zero anywhere.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, truediv_operator)

    def __rtruediv__(
        self,
        other: float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise quotient of this matrix and either
            another matrix or a single number (if this matrix is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        - ZeroDivisionError: If `other` is zero, or is a matrix that
            contains a zero anywhere.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, truediv_operator)

    def __add__(
        self,
        other: Matrix | float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise sum of this matrix and either
            another matrix or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, add_operator)

    def __radd__(
        self,
        other: float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise sum of this matrix and either
            another matrix or a single number (if this matrix is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, add_operator)

    def __sub__(
        self,
        other: Matrix | float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise difference of this matrix and either
            another matrix or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, sub_operator)

    def __rsub__(
        self,
        other: float | Fraction,
    ) -> Matrix:
        """
        Calculates the element-wise difference of this matrix and either
            another matrix or a single number (if this matrix is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Matrix, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, sub_operator)

    def __neg__(
        self,
    ) -> Matrix:
        """
        Calculates the element-wise negation of this matrix.
        """
        return self._elwise_operate(-1, True, mul_operator)

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        """
        Compares this matrix to an object, returns `True` if and only
            if the right-hand side is a matrix with the same dimensions
            as this matrix, such that every element in this matrix is
            equal to every corresponding element in the `other` matrix
            (otherwise returns `False`).

        Arguments
        - other: The object this vector is to be compared to.
        """
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._hash is not None and other._hash is not None:
            if hash(self) != hash(other):
                return False
        if self._shape != other._shape:
            return False
        for row in range(self._shape[0]):
            for col in range(self._shape[1]):
                if self[row, col] != other[row, col]:
                    return False
        return True

    def __or__(
        self,
        other: Matrix,
    ) -> Matrix:
        """
        Augments the rows of this matrix with the rows of the
            `other` matrix.

        Arguments
        - other: The right-hand side rows to append.

        Possible Errors
        - DimensionMismatchError: If the two matrices have unequal row
            counts.
        """
        if not isinstance(other, Matrix):  # type: ignore
            return NotImplemented
        if self._shape[0] != other._shape[0]:
            raise DimensionMismatchError(
                f"left side rows ({self._shape[0]}) "
                f"do not equal right side rows ({other._shape[0]}), "
                "cannot augment columns"
            )
        return Matrix(
            (
                chain(self_row, other_row)
                for self_row, other_row in zip(self._data, other._data)
            )
        )

    def __hash__(
        self,
    ) -> int:
        """
        Returns the hash of this matrix.
        """
        if self._hash is None:
            self._hash = hash(self._data)
        return self._hash

    # PROPERTIES

    @property
    def diagonal(
        self,
    ) -> Iterable[Fraction]:
        for i in range(min(self._shape)):
            yield self._data[i][i]

    @property
    def elements(
        self,
    ) -> list[list[Fraction]]:
        return [[item for item in row] for row in self._data]

    @property
    def shape(
        self,
    ) -> tuple[int, int]:
        return self._shape

    # PRIVATE/PROTECTED METHODS

    def _elwise_operate(
        self,
        other: Matrix | float | Fraction,
        self_side_left: bool,
        operation: Callable[
            [float | Fraction, float | Fraction],
            float | Fraction,
        ],
    ) -> Matrix:
        """
        Returns a matrix that results from the element-wise operation of
            two matrices (or one matrix and a number).

        Arguments
        - other: The right-hand side operand, can be either a matrix or
            a number (numbers are interpreted as homogenous matrices of
            the same shape as `self`).
        - self_side_left: Whether `self` is the left operand (true), or
            the right operand (false).
        - operation: The arbitrary operation applied to two elements to
            create a single result.

        Possible Errors
        - DimensionMismatchError: If `other` is a Matrix and does not
            have the required shape.

        Notes
        - The operation specified in `operation` may raise errors. These
            will not be caught by this method.
        - This is a private method not meant to be exposed.
        """
        if isinstance(other, Matrix):
            if self._shape != other._shape:
                order = (
                    ("left", "right") if self_side_left else ("right", "left")
                )
                raise DimensionMismatchError(
                    f"{order[0]} side shape {self._shape} "
                    f"does not equal {order[1]} side shape {other._shape}"
                )
            if self_side_left:
                return Matrix(
                    (
                        operation(self_item, other_item)
                        for self_item, other_item in zip(*rows)
                    )
                    for rows in zip(self._data, other._data)
                )
            else:
                return Matrix(
                    (
                        operation(other_item, self_item)
                        for self_item, other_item in zip(*rows)
                    )
                    for rows in zip(self._data, other._data)
                )

        else:
            if self_side_left:
                return Matrix(
                    (operation(item, other) for item in row)
                    for row in self._data
                )
            else:
                return Matrix(
                    (operation(other, item) for item in row)
                    for row in self._data
                )

    def _string_format(
        self,
        max_rows: int,
        max_cols: int,
        element_formatter: Callable[[Fraction], str],
    ) -> str:
        """
        Returns a "pretty" string representation of this matrix.

        Arguments
        - max_rows: The maximum number of rows to print.
        - max_cols: The maximum number of columns to print.
        - element_formatter: The operation applied to each element to
            convert it to a string.

        Notes
        - TODO: Refactor to make this more readable.
        - This is a private method not meant to be exposed.
        """

        def format_to_str(n: Fraction, row: int, col: int) -> str:
            if row >= max_rows:
                if col >= max_cols:
                    return "\u22F1"
                return "\u22EE"
            elif col >= max_cols:
                return "\u22EF"
            else:
                return element_formatter(n)

        element_strs = [
            [
                format_to_str(self._data[row][col], row, col)
                for col in range(min(self._shape[1], max_cols + 1))
            ]
            for row in range(min(self._shape[0], max_rows + 1))
        ]
        column_lengths = [
            max(
                (
                    len(element_strs[row][col])
                    for row in range(min(len(element_strs), max_rows + 1))
                )
            )
            for col in range(min(len(element_strs[0]), max_cols + 1))
        ]
        for row in range(len(element_strs)):
            for col in range(len(element_strs[row])):
                element_strs[row][col] = element_strs[row][col].center(
                    column_lengths[col]
                )

        dat_str = f" \u2502\n\u2502 ".join(
            ("  ".join(row) for row in element_strs)
        )
        space = " " * (sum(column_lengths) + (2 * len(column_lengths)))
        return (
            f"\u250C{space}\u2510\n"
            f"\u2502 {dat_str} \u2502"
            f" (size: {self._shape[0]}\u00D7{self._shape[1]})\n"
            f"\u2514{space}\u2518"
        )
