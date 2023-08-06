"""_598.py

LeadModificationSegment
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical import _602
from mastapy._internal.python_net import python_net_import

_LEAD_MODIFICATION_SEGMENT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'LeadModificationSegment')


__docformat__ = 'restructuredtext en'
__all__ = ('LeadModificationSegment',)


class LeadModificationSegment(_602.ModificationSegment):
    """LeadModificationSegment

    This is a mastapy class.
    """

    TYPE = _LEAD_MODIFICATION_SEGMENT

    def __init__(self, instance_to_wrap: 'LeadModificationSegment.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def distance_from_centre(self) -> 'float':
        """float: 'DistanceFromCentre' is the original name of this property."""

        temp = self.wrapped.DistanceFromCentre

        if temp is None:
            return None

        return temp

    @distance_from_centre.setter
    def distance_from_centre(self, value: 'float'):
        self.wrapped.DistanceFromCentre = float(value) if value else 0.0
