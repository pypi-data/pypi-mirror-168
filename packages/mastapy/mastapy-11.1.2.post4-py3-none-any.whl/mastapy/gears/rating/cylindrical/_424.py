"""_424.py

CylindricalGearDutyCycleRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import (
    _433, _425, _426, _443,
    _429
)
from mastapy.gears.rating import _331, _330
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDutyCycleRating',)


class CylindricalGearDutyCycleRating(_330.GearDutyCycleRating):
    """CylindricalGearDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'CylindricalGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def highest_maximum_material_exposure(self) -> 'float':
        """float: 'HighestMaximumMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HighestMaximumMaterialExposure

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_against_permanent_deformation(self) -> 'float':
        """float: 'SafetyFactorAgainstPermanentDeformation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorAgainstPermanentDeformation

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_against_permanent_deformation_with_influence_of_rim(self) -> 'float':
        """float: 'SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim

        if temp is None:
            return None

        return temp

    @property
    def gear_set_design_duty_cycle(self) -> '_433.CylindricalGearSetDutyCycleRating':
        """CylindricalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDesignDutyCycle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_set_design_duty_cycle(self) -> '_433.CylindricalGearSetDutyCycleRating':
        """CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSetDesignDutyCycle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank_rating(self) -> '_331.GearFlankRating':
        """GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlankRating

        if temp is None:
            return None

        if _331.GearFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast left_flank_rating to GearFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank_rating(self) -> '_331.GearFlankRating':
        """GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlankRating

        if temp is None:
            return None

        if _331.GearFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast right_flank_rating to GearFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_mesh_ratings(self) -> 'List[_443.MeshRatingForReports]':
        """List[MeshRatingForReports]: 'CylindricalGearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gear_ratings(self) -> 'List[_429.CylindricalGearRating]':
        """List[CylindricalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_ratings(self) -> 'List[_429.CylindricalGearRating]':
        """List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
