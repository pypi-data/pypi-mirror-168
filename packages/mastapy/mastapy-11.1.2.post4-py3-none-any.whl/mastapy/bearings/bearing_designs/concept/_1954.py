"""_1954.py

ConceptClearanceBearing
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs import _1892
from mastapy._internal.python_net import python_net_import

_CONCEPT_CLEARANCE_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Concept', 'ConceptClearanceBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptClearanceBearing',)


class ConceptClearanceBearing(_1892.NonLinearBearing):
    """ConceptClearanceBearing

    This is a mastapy class.
    """

    TYPE = _CONCEPT_CLEARANCE_BEARING

    def __init__(self, instance_to_wrap: 'ConceptClearanceBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_diameter(self) -> 'float':
        """float: 'ContactDiameter' is the original name of this property."""

        temp = self.wrapped.ContactDiameter

        if temp is None:
            return None

        return temp

    @contact_diameter.setter
    def contact_diameter(self, value: 'float'):
        self.wrapped.ContactDiameter = float(value) if value else 0.0

    @property
    def contact_stiffness(self) -> 'float':
        """float: 'ContactStiffness' is the original name of this property."""

        temp = self.wrapped.ContactStiffness

        if temp is None:
            return None

        return temp

    @contact_stiffness.setter
    def contact_stiffness(self, value: 'float'):
        self.wrapped.ContactStiffness = float(value) if value else 0.0
