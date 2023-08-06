"""_1713.py

LoadedBearingTemperatureChart
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1535
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_TEMPERATURE_CHART = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingTemperatureChart')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingTemperatureChart',)


class LoadedBearingTemperatureChart(_1535.CustomReportChart):
    """LoadedBearingTemperatureChart

    This is a mastapy class.
    """

    TYPE = _LOADED_BEARING_TEMPERATURE_CHART

    def __init__(self, instance_to_wrap: 'LoadedBearingTemperatureChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_temperature(self) -> 'float':
        """float: 'MaximumTemperature' is the original name of this property."""

        temp = self.wrapped.MaximumTemperature

        if temp is None:
            return None

        return temp

    @maximum_temperature.setter
    def maximum_temperature(self, value: 'float'):
        self.wrapped.MaximumTemperature = float(value) if value else 0.0

    @property
    def minimum_temperature(self) -> 'float':
        """float: 'MinimumTemperature' is the original name of this property."""

        temp = self.wrapped.MinimumTemperature

        if temp is None:
            return None

        return temp

    @minimum_temperature.setter
    def minimum_temperature(self, value: 'float'):
        self.wrapped.MinimumTemperature = float(value) if value else 0.0

    @property
    def number_of_steps(self) -> 'int':
        """int: 'NumberOfSteps' is the original name of this property."""

        temp = self.wrapped.NumberOfSteps

        if temp is None:
            return None

        return temp

    @number_of_steps.setter
    def number_of_steps(self, value: 'int'):
        self.wrapped.NumberOfSteps = int(value) if value else 0
