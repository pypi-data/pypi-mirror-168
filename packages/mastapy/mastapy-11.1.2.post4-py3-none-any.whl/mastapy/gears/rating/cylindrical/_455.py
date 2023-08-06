"""_455.py

VDI2737SafetyFactorReportingObject
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_VDI2737_SAFETY_FACTOR_REPORTING_OBJECT = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'VDI2737SafetyFactorReportingObject')


__docformat__ = 'restructuredtext en'
__all__ = ('VDI2737SafetyFactorReportingObject',)


class VDI2737SafetyFactorReportingObject(_0.APIBase):
    """VDI2737SafetyFactorReportingObject

    This is a mastapy class.
    """

    TYPE = _VDI2737_SAFETY_FACTOR_REPORTING_OBJECT

    def __init__(self, instance_to_wrap: 'VDI2737SafetyFactorReportingObject.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def crack_initiation(self) -> 'float':
        """float: 'CrackInitiation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrackInitiation

        if temp is None:
            return None

        return temp

    @property
    def fatigue_fracture(self) -> 'float':
        """float: 'FatigueFracture' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueFracture

        if temp is None:
            return None

        return temp

    @property
    def permanent_deformation(self) -> 'float':
        """float: 'PermanentDeformation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermanentDeformation

        if temp is None:
            return None

        return temp
