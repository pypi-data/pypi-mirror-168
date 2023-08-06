"""_2237.py

ConcentricPartGroup
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._math.vector_2d import Vector2D
from mastapy.system_model.part_model.part_groups import _2238, _2236
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricPartGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroup',)


class ConcentricPartGroup(_2236.ConcentricOrParallelPartGroup):
    """ConcentricPartGroup

    This is a mastapy class.
    """

    TYPE = _CONCENTRIC_PART_GROUP

    def __init__(self, instance_to_wrap: 'ConcentricPartGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_of_cylindrical_gear_face_widths(self) -> 'float':
        """float: 'TotalOfCylindricalGearFaceWidths' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalOfCylindricalGearFaceWidths

        if temp is None:
            return None

        return temp

    @property
    def radial_position(self) -> 'Vector2D':
        """Vector2D: 'RadialPosition' is the original name of this property."""

        temp = self.wrapped.RadialPosition

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @radial_position.setter
    def radial_position(self, value: 'Vector2D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector2d(value)
        self.wrapped.RadialPosition = value

    @property
    def parallel_groups(self) -> 'List[_2238.ConcentricPartGroupParallelToThis]':
        """List[ConcentricPartGroupParallelToThis]: 'ParallelGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParallelGroups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
