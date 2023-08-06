import abc
import typing

from goats.core import algebraic
from goats.core import metadata


# This should support algebraic operations on metadata attributes without
# knowledge of the type of interface. Some guiding use cases:
# - If the interface is an instance of `variable.Quantity`, `implement` should
#   evaluate it with `func` (see `measurable.Quantified.implement`).
# - If the interface is an instance of `computable.Quantity`, `implement` should
#   do nothing.
class Base(algebraic.Quantity):
    """The base quantity."""
    def __init__(self, __interface) -> None:
        self._interface = __interface
        self._meta = None

    @property
    def meta(self):
        """This quantity's metadata attributes."""
        if self._meta is None:
            self._meta = metadata.OperatorFactory(type(self))
        return self._meta

    def __eq__(self, other) -> bool:
        """Called for self == other."""
        for name in self.meta.parameters:
            v = getattr(self, name)
            if hasattr(other, name) and getattr(other, name) != v:
                return False
        return True

    def implement(self, func: typing.Callable, mode: str, *others, **kwargs):
        """Implement a standard operation."""
        name = func.__name__
        if mode == 'cast':
            return self.compute(func, mode)
        if mode == 'arithmetic':
            data = self.compute(func, mode, **kwargs)
            meta = self.meta[name].evaluate(self, **kwargs)
            return type(self)(data, **meta)
        operands = [self] + list(others)
        args = [
            self.compute(func, mode, **kwargs)
            if isinstance(i, Base) else i
            for i in operands
        ]
        if mode == 'comparison':
            self.meta.check(self, *others)
            return self.compute(func, mode, *args)
        if mode == 'forward':
            data = self.compute(func, mode, *args, **kwargs)
            meta = self.meta[name].evaluate(*operands, **kwargs)
            return type(self)(data, **meta)
        if mode == 'reverse':
            data = self.compute(func, mode, *reversed(args), **kwargs)
            meta = self.meta[name].evaluate(*reversed(operands), **kwargs)
            return type(self)(data, **meta)
        if mode == 'inplace':
            data = self.compute(func, mode, *args, **kwargs)
            meta = self.meta[name].evaluate(*operands, **kwargs)
            self._data = data
            for k, v in meta:
                setattr(self, k, v)
            return self
        raise ValueError(f"Unknown operator mode {mode!r}")

    @abc.abstractmethod
    def compute(self, func: typing.Callable, mode: str, *args, **kwargs):
        """Evaluate this quantity's data interface."""
        pass


