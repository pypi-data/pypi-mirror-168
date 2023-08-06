"""_52.py

CylindricalMisalignmentCalculator
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MISALIGNMENT_CALCULATOR = python_net_import('SMT.MastaAPI.NodalAnalysis', 'CylindricalMisalignmentCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMisalignmentCalculator',)


class CylindricalMisalignmentCalculator(_0.APIBase):
    """CylindricalMisalignmentCalculator

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MISALIGNMENT_CALCULATOR

    def __init__(self, instance_to_wrap: 'CylindricalMisalignmentCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_a_equivalent_misalignment_for_rating(self) -> 'float':
        """float: 'GearAEquivalentMisalignmentForRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAEquivalentMisalignmentForRating

        if temp is None:
            return None

        return temp

    @property
    def gear_a_line_fit_misalignment(self) -> 'float':
        """float: 'GearALineFitMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearALineFitMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_a_line_fit_misalignment_angle(self) -> 'float':
        """float: 'GearALineFitMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearALineFitMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def gear_a_radial_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'GearARadialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearARadialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_a_rigid_body_misalignment(self) -> 'float':
        """float: 'GearARigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearARigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_a_rigid_body_misalignment_angle(self) -> 'float':
        """float: 'GearARigidBodyMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearARigidBodyMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def gear_a_single_node_misalignment_angle_due_to_tilt(self) -> 'float':
        """float: 'GearASingleNodeMisalignmentAngleDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearASingleNodeMisalignmentAngleDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def gear_a_single_node_misalignment_due_to_tilt(self) -> 'float':
        """float: 'GearASingleNodeMisalignmentDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearASingleNodeMisalignmentDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def gear_a_single_node_misalignment_due_to_twist(self) -> 'float':
        """float: 'GearASingleNodeMisalignmentDueToTwist' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearASingleNodeMisalignmentDueToTwist

        if temp is None:
            return None

        return temp

    @property
    def gear_a_tangential_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'GearATangentialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearATangentialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_a_transverse_separations(self) -> 'List[float]':
        """List[float]: 'GearATransverseSeparations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearATransverseSeparations

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def gear_b_equivalent_misalignment_for_rating(self) -> 'float':
        """float: 'GearBEquivalentMisalignmentForRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBEquivalentMisalignmentForRating

        if temp is None:
            return None

        return temp

    @property
    def gear_b_line_fit_misalignment(self) -> 'float':
        """float: 'GearBLineFitMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBLineFitMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_b_line_fit_misalignment_angle(self) -> 'float':
        """float: 'GearBLineFitMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBLineFitMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def gear_b_radial_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'GearBRadialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBRadialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_b_rigid_body_misalignment(self) -> 'float':
        """float: 'GearBRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_b_rigid_body_misalignment_angle(self) -> 'float':
        """float: 'GearBRigidBodyMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBRigidBodyMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def gear_b_single_node_misalignment_angle_due_to_tilt(self) -> 'float':
        """float: 'GearBSingleNodeMisalignmentAngleDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBSingleNodeMisalignmentAngleDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def gear_b_single_node_misalignment_due_to_tilt(self) -> 'float':
        """float: 'GearBSingleNodeMisalignmentDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBSingleNodeMisalignmentDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def gear_b_single_node_misalignment_due_to_twist(self) -> 'float':
        """float: 'GearBSingleNodeMisalignmentDueToTwist' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBSingleNodeMisalignmentDueToTwist

        if temp is None:
            return None

        return temp

    @property
    def gear_b_tangential_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'GearBTangentialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBTangentialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def gear_b_transverse_separations(self) -> 'List[float]':
        """List[float]: 'GearBTransverseSeparations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBTransverseSeparations

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def total_equivalent_misalignment_for_rating(self) -> 'float':
        """float: 'TotalEquivalentMisalignmentForRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalEquivalentMisalignmentForRating

        if temp is None:
            return None

        return temp

    @property
    def total_line_fit_misalignment(self) -> 'float':
        """float: 'TotalLineFitMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalLineFitMisalignment

        if temp is None:
            return None

        return temp

    @property
    def total_line_fit_misalignment_angle(self) -> 'float':
        """float: 'TotalLineFitMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalLineFitMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def total_radial_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'TotalRadialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalRadialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def total_rigid_body_misalignment(self) -> 'float':
        """float: 'TotalRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def total_rigid_body_misalignment_angle(self) -> 'float':
        """float: 'TotalRigidBodyMisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalRigidBodyMisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def total_single_node_misalignment(self) -> 'float':
        """float: 'TotalSingleNodeMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSingleNodeMisalignment

        if temp is None:
            return None

        return temp

    @property
    def total_single_node_misalignment_angle_due_to_tilt(self) -> 'float':
        """float: 'TotalSingleNodeMisalignmentAngleDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSingleNodeMisalignmentAngleDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def total_single_node_misalignment_due_to_tilt(self) -> 'float':
        """float: 'TotalSingleNodeMisalignmentDueToTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSingleNodeMisalignmentDueToTilt

        if temp is None:
            return None

        return temp

    @property
    def total_single_node_misalignment_due_to_twist(self) -> 'float':
        """float: 'TotalSingleNodeMisalignmentDueToTwist' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSingleNodeMisalignmentDueToTwist

        if temp is None:
            return None

        return temp

    @property
    def total_tangential_angular_component_of_rigid_body_misalignment(self) -> 'float':
        """float: 'TotalTangentialAngularComponentOfRigidBodyMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalTangentialAngularComponentOfRigidBodyMisalignment

        if temp is None:
            return None

        return temp

    @property
    def rigid_body_coordinate_system_x_axis(self) -> 'Vector3D':
        """Vector3D: 'RigidBodyCoordinateSystemXAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RigidBodyCoordinateSystemXAxis

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def rigid_body_coordinate_system_y_axis(self) -> 'Vector3D':
        """Vector3D: 'RigidBodyCoordinateSystemYAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RigidBodyCoordinateSystemYAxis

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value
