"""_1058.py

CylindricalGearMeshMicroGeometryDutyCycle
"""


from typing import List

from mastapy.gears.rating.cylindrical import _433
from mastapy._internal import constructor, conversion
from mastapy.gears.ltca.cylindrical import _823
from mastapy.gears.analysis import _1174
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMeshMicroGeometryDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMicroGeometryDutyCycle',)


class CylindricalGearMeshMicroGeometryDutyCycle(_1174.GearMeshDesignAnalysis):
    """CylindricalGearMeshMicroGeometryDutyCycle

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMicroGeometryDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cylindrical_gear_set_duty_cycle_rating(self) -> '_433.CylindricalGearSetDutyCycleRating':
        """CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSetDutyCycleRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def meshes_analysis(self) -> 'List[_823.CylindricalGearMeshLoadDistributionAnalysis]':
        """List[CylindricalGearMeshLoadDistributionAnalysis]: 'MeshesAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshesAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
