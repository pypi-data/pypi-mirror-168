import typing

from goats.core import axis
from goats.core import datafile
from goats.core import metric
from goats.core import variable


class Interface:
    """"""

    def __init__(
        self,
        __datafile: datafile.Interface,
        system: typing.Union[str, metric.System]=None,
    ) -> None:
        self._datafile = __datafile
        self._system = system
        self._axes = None
        self._variables = None

    @property
    def axes(self):
        """An interface to this dataset's axis quantities."""
        if self._axes is None:
            self._axes = axis.Interface(self._datafile, self.system)
        return self._axes

    @property
    def variables(self):
        """An interface to this dataset's variable quantities."""
        if self._variables is None:
            self._variables = variable.Interface(self._datafile, self.system)
        return self._variables

    @property
    def system(self):
        """This dataset's metric system."""
        return self._system
