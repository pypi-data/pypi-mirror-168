"""_909.py

DesignConstraintsCollection
"""


from typing import List

from mastapy.utility.property import _1612
from mastapy.gears.gear_designs import _907
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINTS_COLLECTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintsCollection')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintsCollection',)


class DesignConstraintsCollection(_1605.NamedDatabaseItem):
    """DesignConstraintsCollection

    This is a mastapy class.
    """

    TYPE = _DESIGN_CONSTRAINTS_COLLECTION

    def __init__(self, instance_to_wrap: 'DesignConstraintsCollection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints(self) -> 'List[_1612.DeletableCollectionMember[_907.DesignConstraint]]':
        """List[DeletableCollectionMember[DesignConstraint]]: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignConstraints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
