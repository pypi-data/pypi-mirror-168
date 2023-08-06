"""_1833.py

ThreePointContactInternalClearance
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1735
from mastapy._internal.python_net import python_net_import

_THREE_POINT_CONTACT_INTERNAL_CLEARANCE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ThreePointContactInternalClearance')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreePointContactInternalClearance',)


class ThreePointContactInternalClearance(_1735.InternalClearance):
    """ThreePointContactInternalClearance

    This is a mastapy class.
    """

    TYPE = _THREE_POINT_CONTACT_INTERNAL_CLEARANCE

    def __init__(self, instance_to_wrap: 'ThreePointContactInternalClearance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def operating_free_contact_angle(self) -> 'float':
        """float: 'OperatingFreeContactAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingFreeContactAngle

        if temp is None:
            return None

        return temp
