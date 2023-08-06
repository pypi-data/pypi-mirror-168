"""
Implements the `Vector` class (see `help(Vector)`).
"""

from __future__ import annotations

from fractions import Fraction
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

__all__ = ("Vector",)


class Vector(
    HashableABC,
    SequenceABC[Fraction],
):
    """
    Expresses the mathematical notion of a rational-valued Vector in
        native Python datastructures and datatypes while providing an
        assortment of tools to perform basic vector manipulations.

    `Vector` objects are considered non-mutable, which means that for
        the life of an object it cannot be meaningfully modified[^1].
        Vectors are, therefore, hashable (using
        `hash(vector_instance)`).

    [^1]: If you need to modify a `Vector`, look into the
        `vector_instance.elements` property.
    """

    __slots__ = (
        "_data",
        "_length",
        "_hash",
    )

    def __init__(
        self,
        initializer: Iterable[float | Fraction],
    ) -> None:
        """
        Initializes a new instance of the `Vector` class.

        Arguments
        - initializer: An iterable that will be used to construct the
            vector.

        Possible Errors
        - ValueError: If the initializer has no elements.
        """
        data = tuple(Fraction(item) for item in initializer)
        if len(data) <= 0:
            raise ValueError("vectors must have at least one element")
        self._data: Final[tuple[Fraction, ...]] = data
        self._length: Final[int] = len(data)
        self._hash: int | None = None

    def __len__(
        self,
    ) -> int:
        """
        Returns the total number of elements in this vector.
        """
        return self._length

    @overload
    def __getitem__(self, key: int) -> Fraction:
        ...

    @overload
    def __getitem__(self, key: slice) -> Vector:
        ...

    def __getitem__(
        self,
        key: int | slice,
    ) -> Fraction | Vector:
        """
        Returns a copy of the items at given positions.

        Arguments
        - key: The 0-indexed position of the desired elements.

        Possible Errors
        - IndexError: If the slice would create a vector with zero
            elements, or if an integer index is out of bounds.
        """
        try:
            if isinstance(key, int):
                return self._data[key]
            else:
                return Vector(self._data[key])
        except IndexError:
            raise IndexError(
                f"index out of bounds, expected index in "
                f"[0, {self._length}) but received {key}"
            )

    def __iter__(
        self,
    ) -> Iterator[Fraction]:
        """
        Returns an iterator over the items of this vector.
        """
        return self._data.__iter__()

    def __str__(
        self,
    ) -> str:
        """
        Returns a "pretty" string representation of this vector.
        """
        return self._string_format(
            10,
            lambda f: (
                "%.3g" % (f.numerator if f.denominator == 1 else float(f))
            ),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Returns a reproduction string representation of this vector.
        """
        obj_name = self.__class__.__name__
        initializer = "[{}]".format(
            ", ".join(repr(item) for item in self._data)
        )
        return f"{obj_name}(\n    initializer={initializer},\n)"

    def __matmul__(
        self,
        other: Vector,
    ) -> Fraction:
        """
        Calculates the dot product of this and another vector.

        Arguments
        - other: The right-hand-side operand to dot multiplication.

        Possible Errors
        - DimensionMismatchError: If the two vectors have different
            lengths.

        Notes
        - To calculate the element-wise product of two vectors, use the
            `__mul__` (asterisk) operator.
        """
        if not isinstance(other, Vector):  # type: ignore
            return NotImplemented
        if self._length != other._length:
            raise DimensionMismatchError(
                f"left side length ({self._length}) "
                f"does not match right side length ({other._length})"
            )
        return sum(
            (
                self_item * other_item
                for self_item, other_item in zip(self._data, other._data)
            ),
            start=Fraction(0),
        )

    def __mul__(
        self,
        other: Vector | float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise product of this vector and either
            another vector or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.

        Notes
        - To calculate the dot product of two matrices, use the
            `__matmul__` (at-sign) operator.
        """

        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, mul_operator)

    def __rmul__(
        self,
        other: float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise product of this vector and either
            another vector or a single number (if this vector is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.

        Notes
        - To calculate the dot product of two matrices, use the
            `__matmul__` (at-sign) operator.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, mul_operator)

    def __truediv__(
        self,
        other: Vector | float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise quotient of this vector and either
            another vector or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        - ZeroDivisionError: If `other` is zero, or is a vector that
            contains a zero anywhere.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, truediv_operator)

    def __rtruediv__(
        self,
        other: float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise quotient of this vector and either
            another vector or a single number (if this vector is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        - ZeroDivisionError: If `other` is zero, or is a vector that
            contains a zero anywhere.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, truediv_operator)

    def __add__(
        self,
        other: Vector | float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise sum of this vector and either
            another vector or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, add_operator)

    def __radd__(
        self,
        other: float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise sum of this vector and either
            another vector or a single number (if this vector is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, add_operator)

    def __sub__(
        self,
        other: Vector | float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise difference of this vector and either
            another vector or a single number.

        Arguments
        - other: The left-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, True, sub_operator)

    def __rsub__(
        self,
        other: float | Fraction,
    ) -> Vector:
        """
        Calculates the element-wise difference of this vector and either
            another vector or a single number (if this vector is the
            right-hand-side operand).

        Arguments
        - other: The right-hand-side operand.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.
        """
        if not isinstance(
            other,
            (Vector, int, float, Fraction),
        ):  # type: ignore
            return NotImplemented
        return self._elwise_operate(other, False, sub_operator)

    def __neg__(
        self,
    ) -> Vector:
        """
        Calculates the element-wise negation of this vector.
        """
        return self._elwise_operate(-1, True, mul_operator)

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        """
        Compares this vector to an object, returns true if and only
            if the right-hand side is a vector with the same length
            as this vector, such that every element in this vector is
            equal to every corresponding element in the `other` vector
            (otherwise returns false).

        Arguments
        - other: The object this vector is to be compared to.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        if self._hash is not None and other._hash is not None:
            if hash(self) != hash(other):
                return False
        length = self._length
        if length != other._length:
            return False
        for i in range(length):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __hash__(
        self,
    ) -> int:
        """
        Returns the hash of this vector.
        """
        if self._hash is None:
            self._hash = hash(self._data)
        return self._hash

    # PROPERTIES

    @property
    def elements(
        self,
    ) -> list[Fraction]:
        return [item for item in self._data]

    # PRIVATE/PROTECTED METHODS

    def _elwise_operate(
        self,
        other: Vector | float | Fraction,
        self_side_left: bool,
        operation: Callable[
            [float | Fraction, float | Fraction],
            float | Fraction,
        ],
    ) -> Vector:
        """
        Creates and returns a vector that results from the element-
            wise operation of two matrices (or one vector and a number).

        Arguments
        - other: The right-hand side operand, can be either a vector or
            a number (numbers are interpreted as homogenous matrices of
            the same shape as `self`).
        - self_side_left: Whether `self` is the left operand (true), or
            the right operand (false).
        - operation: The arbitrary operation applied to two elements to
            create a single result.

        Possible Errors
        - DimensionMismatchError: If `other` is a Vector and does not
            have the required shape.

        Notes
        - The operation specified in `operation` may raise errors. These
            will not be caught by this method.
        - This is a private method not meant to be exposed.
        """
        if isinstance(other, Vector):
            if self._length != other._length:
                order = (
                    ("left", "right") if self_side_left else ("right", "left")
                )
                raise DimensionMismatchError(
                    f"{order[0]} side length {self._length} "
                    f"does not equal {order[1]} side length {other._length}"
                )
            if self_side_left:
                return Vector(
                    operation(self_item, other_item)
                    for self_item, other_item in zip(self._data, other._data)
                )
            else:
                return Vector(
                    operation(other_item, self_item)
                    for self_item, other_item in zip(self._data, other._data)
                )
        else:
            if self_side_left:
                return Vector(operation(item, other) for item in self._data)
            else:
                return Vector(operation(other, item) for item in self._data)

    def _string_format(
        self,
        max_elements: int,
        element_formatter: Callable[[Fraction], str],
    ) -> str:
        """
        Returns a "pretty" string representation of this vector.

        Arguments
        - max_elements: The maximum number of elements to print.
        - element_formatter: The operation applied to each element to
            convert it to a string.

        Notes
        - TODO: Refactor to make this more readable.
        - This is a private method not meant to be exposed.
        """

        def format_as_str(n: Fraction, idx: int) -> str:
            if idx >= max_elements:
                return "\u22EF"
            else:
                return element_formatter(n)

        return (
            f"\u27E8 "
            + ", ".join(
                (
                    format_as_str(self._data[element], element)
                    for element in range(min(self._length, max_elements + 1))
                )
            )
            + f" \u27E9 (size: {self._length})"
        )
