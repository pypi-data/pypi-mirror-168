"""_2306.py

PressureRatioInputOptions
"""


from mastapy._internal import constructor
from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_PRESSURE_RATIO_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'PressureRatioInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PressureRatioInputOptions',)


class PressureRatioInputOptions(_1622.ColumnInputOptions):
    """PressureRatioInputOptions

    This is a mastapy class.
    """

    TYPE = _PRESSURE_RATIO_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'PressureRatioInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reference_pressure(self) -> 'float':
        """float: 'ReferencePressure' is the original name of this property."""

        temp = self.wrapped.ReferencePressure

        if temp is None:
            return None

        return temp

    @reference_pressure.setter
    def reference_pressure(self, value: 'float'):
        self.wrapped.ReferencePressure = float(value) if value else 0.0
