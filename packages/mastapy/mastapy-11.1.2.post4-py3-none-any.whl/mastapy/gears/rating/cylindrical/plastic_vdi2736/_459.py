"""_459.py

PlasticGearVDI2736AbstractMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import _1048
from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _458
from mastapy.gears.rating.cylindrical.iso6336 import _485
from mastapy._internal.python_net import python_net_import

_PLASTIC_GEAR_VDI2736_ABSTRACT_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736', 'PlasticGearVDI2736AbstractMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('PlasticGearVDI2736AbstractMeshSingleFlankRating',)


class PlasticGearVDI2736AbstractMeshSingleFlankRating(_485.ISO6336AbstractMeshSingleFlankRating):
    """PlasticGearVDI2736AbstractMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _PLASTIC_GEAR_VDI2736_ABSTRACT_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'PlasticGearVDI2736AbstractMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def air_temperature_ambient_and_assembly(self) -> 'float':
        """float: 'AirTemperatureAmbientAndAssembly' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AirTemperatureAmbientAndAssembly

        if temp is None:
            return None

        return temp

    @property
    def coefficient_of_friction(self) -> 'float':
        """float: 'CoefficientOfFriction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFriction

        if temp is None:
            return None

        return temp

    @property
    def degree_of_tooth_loss(self) -> 'float':
        """float: 'DegreeOfToothLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DegreeOfToothLoss

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_bending(self) -> 'float':
        """float: 'FaceLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_contact(self) -> 'float':
        """float: 'FaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def factor_for_tooth_flank_loading(self) -> 'float':
        """float: 'FactorForToothFlankLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FactorForToothFlankLoading

        if temp is None:
            return None

        return temp

    @property
    def factor_for_tooth_root_load(self) -> 'float':
        """float: 'FactorForToothRootLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FactorForToothRootLoad

        if temp is None:
            return None

        return temp

    @property
    def heat_dissipating_surface_of_housing(self) -> 'float':
        """float: 'HeatDissipatingSurfaceOfHousing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeatDissipatingSurfaceOfHousing

        if temp is None:
            return None

        return temp

    @property
    def heat_transfer_resistance_of_housing(self) -> 'float':
        """float: 'HeatTransferResistanceOfHousing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeatTransferResistanceOfHousing

        if temp is None:
            return None

        return temp

    @property
    def helix_angle_factor_contact(self) -> 'float':
        """float: 'HelixAngleFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleFactorContact

        if temp is None:
            return None

        return temp

    @property
    def percentage_of_openings_in_the_housing_surface(self) -> 'float':
        """float: 'PercentageOfOpeningsInTheHousingSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PercentageOfOpeningsInTheHousingSurface

        if temp is None:
            return None

        return temp

    @property
    def rating_standard_name(self) -> 'str':
        """str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingStandardName

        if temp is None:
            return None

        return temp

    @property
    def relative_tooth_engagement_time(self) -> 'float':
        """float: 'RelativeToothEngagementTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeToothEngagementTime

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_bending(self) -> 'float':
        """float: 'TransverseLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_contact(self) -> 'float':
        """float: 'TransverseLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def type_of_mechanism_housing(self) -> '_1048.TypeOfMechanismHousing':
        """TypeOfMechanismHousing: 'TypeOfMechanismHousing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TypeOfMechanismHousing

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1048.TypeOfMechanismHousing)(value) if value is not None else None

    @property
    def wear_coefficient(self) -> 'float':
        """float: 'WearCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WearCoefficient

        if temp is None:
            return None

        return temp

    @property
    def isodin_cylindrical_gear_single_flank_ratings(self) -> 'List[_458.PlasticGearVDI2736AbstractGearSingleFlankRating]':
        """List[PlasticGearVDI2736AbstractGearSingleFlankRating]: 'ISODINCylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def plastic_vdi2736_cylindrical_gear_single_flank_ratings(self) -> 'List[_458.PlasticGearVDI2736AbstractGearSingleFlankRating]':
        """List[PlasticGearVDI2736AbstractGearSingleFlankRating]: 'PlasticVDI2736CylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlasticVDI2736CylindricalGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
