"""_1836.py

AdjustmentFactors
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ADJUSTMENT_FACTORS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'AdjustmentFactors')


__docformat__ = 'restructuredtext en'
__all__ = ('AdjustmentFactors',)


class AdjustmentFactors(_0.APIBase):
    """AdjustmentFactors

    This is a mastapy class.
    """

    TYPE = _ADJUSTMENT_FACTORS

    def __init__(self, instance_to_wrap: 'AdjustmentFactors.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def for_bearing_load_p(self) -> 'float':
        """float: 'ForBearingLoadP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForBearingLoadP

        if temp is None:
            return None

        return temp

    @property
    def oil_viscosity(self) -> 'float':
        """float: 'OilViscosity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilViscosity

        if temp is None:
            return None

        return temp
