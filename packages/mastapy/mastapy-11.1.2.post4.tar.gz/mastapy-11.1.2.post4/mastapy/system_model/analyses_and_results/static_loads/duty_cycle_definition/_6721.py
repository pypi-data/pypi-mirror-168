"""_6721.py

GearRatioInputOptions
"""


from mastapy._internal import constructor
from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_GEAR_RATIO_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'GearRatioInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearRatioInputOptions',)


class GearRatioInputOptions(_1622.ColumnInputOptions):
    """GearRatioInputOptions

    This is a mastapy class.
    """

    TYPE = _GEAR_RATIO_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'GearRatioInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def has_gear_ratio_column(self) -> 'bool':
        """bool: 'HasGearRatioColumn' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasGearRatioColumn

        if temp is None:
            return None

        return temp

    @property
    def tolerance(self) -> 'float':
        """float: 'Tolerance' is the original name of this property."""

        temp = self.wrapped.Tolerance

        if temp is None:
            return None

        return temp

    @tolerance.setter
    def tolerance(self, value: 'float'):
        self.wrapped.Tolerance = float(value) if value else 0.0
