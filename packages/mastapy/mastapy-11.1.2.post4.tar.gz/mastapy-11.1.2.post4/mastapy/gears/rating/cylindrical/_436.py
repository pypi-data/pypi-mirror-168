"""_436.py

CylindricalMeshDutyCycleRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import _427
from mastapy.gears.rating import _337
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalMeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshDutyCycleRating',)


class CylindricalMeshDutyCycleRating(_337.MeshDutyCycleRating):
    """CylindricalMeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MESH_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'CylindricalMeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_nominal_axial_force(self) -> 'float':
        """float: 'MaximumNominalAxialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNominalAxialForce

        if temp is None:
            return None

        return temp

    @property
    def maximum_nominal_tangential_load(self) -> 'float':
        """float: 'MaximumNominalTangentialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNominalTangentialLoad

        if temp is None:
            return None

        return temp

    @property
    def maximum_radial_separating_load(self) -> 'float':
        """float: 'MaximumRadialSeparatingLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRadialSeparatingLoad

        if temp is None:
            return None

        return temp

    @property
    def micropitting_safety_factor(self) -> 'float':
        """float: 'MicropittingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def permanent_deformation_safety_factor_step_1(self) -> 'float':
        """float: 'PermanentDeformationSafetyFactorStep1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermanentDeformationSafetyFactorStep1

        if temp is None:
            return None

        return temp

    @property
    def permanent_deformation_safety_factor_step_2(self) -> 'float':
        """float: 'PermanentDeformationSafetyFactorStep2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermanentDeformationSafetyFactorStep2

        if temp is None:
            return None

        return temp

    @property
    def scuffing_load_safety_factor_integral_temperature_method(self) -> 'float':
        """float: 'ScuffingLoadSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingLoadSafetyFactorIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def scuffing_safety_factor_flash_temperature_method(self) -> 'float':
        """float: 'ScuffingSafetyFactorFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def scuffing_safety_factor_integral_temperature_method(self) -> 'float':
        """float: 'ScuffingSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorIntegralTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def highest_torque_load_case(self) -> '_427.CylindricalGearMeshRating':
        """CylindricalGearMeshRating: 'HighestTorqueLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HighestTorqueLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_ratings(self) -> 'List[_427.CylindricalGearMeshRating]':
        """List[CylindricalGearMeshRating]: 'CylindricalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def loaded_cylindrical_mesh_ratings(self) -> 'List[_427.CylindricalGearMeshRating]':
        """List[CylindricalGearMeshRating]: 'LoadedCylindricalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedCylindricalMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
