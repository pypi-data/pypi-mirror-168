"""_390.py

KlingelnbergCycloPalloidHypoidMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.klingelnberg_conical.kn3030 import _389, _386
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030', 'KlingelnbergCycloPalloidHypoidMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidMeshSingleFlankRating',)


class KlingelnbergCycloPalloidHypoidMeshSingleFlankRating(_386.KlingelnbergConicalMeshSingleFlankRating):
    """KlingelnbergCycloPalloidHypoidMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_ratio_factor_scuffing(self) -> 'float':
        """float: 'ContactRatioFactorScuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorScuffing

        if temp is None:
            return None

        return temp

    @property
    def curvature_radius(self) -> 'float':
        """float: 'CurvatureRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurvatureRadius

        if temp is None:
            return None

        return temp

    @property
    def dynamic_factor(self) -> 'float':
        """float: 'DynamicFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactor

        if temp is None:
            return None

        return temp

    @property
    def friction_coefficient(self) -> 'float':
        """float: 'FrictionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrictionCoefficient

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor(self) -> 'float':
        """float: 'GeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def integral_flash_temperature(self) -> 'float':
        """float: 'IntegralFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntegralFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor_transverse(self) -> 'float':
        """float: 'LoadDistributionFactorTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorTransverse

        if temp is None:
            return None

        return temp

    @property
    def relating_factor_for_the_thermal_flash_temperature(self) -> 'float':
        """float: 'RelatingFactorForTheThermalFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelatingFactorForTheThermalFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def sliding_factor(self) -> 'float':
        """float: 'SlidingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingFactor

        if temp is None:
            return None

        return temp

    @property
    def tangential_speed_sum(self) -> 'float':
        """float: 'TangentialSpeedSum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialSpeedSum

        if temp is None:
            return None

        return temp

    @property
    def total_speed_in_depthwise_direction(self) -> 'float':
        """float: 'TotalSpeedInDepthwiseDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSpeedInDepthwiseDirection

        if temp is None:
            return None

        return temp

    @property
    def total_speed_in_lengthwise_direction(self) -> 'float':
        """float: 'TotalSpeedInLengthwiseDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSpeedInLengthwiseDirection

        if temp is None:
            return None

        return temp

    @property
    def gear_single_flank_ratings(self) -> 'List[_389.KlingelnbergCycloPalloidHypoidGearSingleFlankRating]':
        """List[KlingelnbergCycloPalloidHypoidGearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def kn3030_klingelnberg_gear_single_flank_ratings(self) -> 'List[_389.KlingelnbergCycloPalloidHypoidGearSingleFlankRating]':
        """List[KlingelnbergCycloPalloidHypoidGearSingleFlankRating]: 'KN3030KlingelnbergGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KN3030KlingelnbergGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
