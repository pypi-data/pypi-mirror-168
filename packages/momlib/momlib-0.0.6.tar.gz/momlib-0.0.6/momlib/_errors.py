"""
Provides definitions and implementations that need to be available to
    all modules that implement linear algebra functionality.
"""

__all__ = (
    "LinearDependenceError",
    "RectangularMatrixError",
    "DimensionMismatchError",
)


class DimensionMismatchError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class LinearDependenceError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class RectangularMatrixError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)
