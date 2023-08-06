"""_1835.py

AdjustedSpeed
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1836, _1855
from mastapy._internal.python_net import python_net_import

_ADJUSTED_SPEED = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'AdjustedSpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AdjustedSpeed',)


class AdjustedSpeed(_1855.SKFCalculationResult):
    """AdjustedSpeed

    This is a mastapy class.
    """

    TYPE = _ADJUSTED_SPEED

    def __init__(self, instance_to_wrap: 'AdjustedSpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def adjusted_reference_speed(self) -> 'float':
        """float: 'AdjustedReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdjustedReferenceSpeed

        if temp is None:
            return None

        return temp

    @property
    def adjustment_factors(self) -> '_1836.AdjustmentFactors':
        """AdjustmentFactors: 'AdjustmentFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdjustmentFactors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
