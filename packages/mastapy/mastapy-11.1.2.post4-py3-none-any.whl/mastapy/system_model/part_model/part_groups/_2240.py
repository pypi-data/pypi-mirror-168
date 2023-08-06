"""_2240.py

ParallelPartGroup
"""


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.part_groups import _2237, _2239, _2236
from mastapy._internal.python_net import python_net_import

_PARALLEL_PART_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ParallelPartGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ParallelPartGroup',)


class ParallelPartGroup(_2236.ConcentricOrParallelPartGroup):
    """ParallelPartGroup

    This is a mastapy class.
    """

    TYPE = _PARALLEL_PART_GROUP

    def __init__(self, instance_to_wrap: 'ParallelPartGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def two_dx_axis_direction(self) -> 'Vector3D':
        """Vector3D: 'TwoDXAxisDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TwoDXAxisDirection

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def two_dy_axis_direction(self) -> 'Vector3D':
        """Vector3D: 'TwoDYAxisDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TwoDYAxisDirection

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def two_dz_axis_direction(self) -> 'Vector3D':
        """Vector3D: 'TwoDZAxisDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TwoDZAxisDirection

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def concentric_part_groups(self) -> 'List[_2237.ConcentricPartGroup]':
        """List[ConcentricPartGroup]: 'ConcentricPartGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConcentricPartGroups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def design_measurements(self) -> 'List[_2239.DesignMeasurements]':
        """List[DesignMeasurements]: 'DesignMeasurements' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignMeasurements

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
