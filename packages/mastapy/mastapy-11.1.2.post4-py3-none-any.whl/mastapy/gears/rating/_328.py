"""_328.py

BendingAndContactReportingObject
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BENDING_AND_CONTACT_REPORTING_OBJECT = python_net_import('SMT.MastaAPI.Gears.Rating', 'BendingAndContactReportingObject')


__docformat__ = 'restructuredtext en'
__all__ = ('BendingAndContactReportingObject',)


class BendingAndContactReportingObject(_0.APIBase):
    """BendingAndContactReportingObject

    This is a mastapy class.
    """

    TYPE = _BENDING_AND_CONTACT_REPORTING_OBJECT

    def __init__(self, instance_to_wrap: 'BendingAndContactReportingObject.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending(self) -> 'float':
        """float: 'Bending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bending

        if temp is None:
            return None

        return temp

    @property
    def contact(self) -> 'float':
        """float: 'Contact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Contact

        if temp is None:
            return None

        return temp
