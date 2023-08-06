"""_526.py

GleasonSpiralBevelMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.bevel.standards import _525, _528
from mastapy._internal.python_net import python_net_import

_GLEASON_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'GleasonSpiralBevelMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GleasonSpiralBevelMeshSingleFlankRating',)


class GleasonSpiralBevelMeshSingleFlankRating(_528.SpiralBevelMeshSingleFlankRating):
    """GleasonSpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _GLEASON_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'GleasonSpiralBevelMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_scoring_index(self) -> 'float':
        """float: 'AllowableScoringIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableScoringIndex

        if temp is None:
            return None

        return temp

    @property
    def assumed_maximum_pinion_torque(self) -> 'float':
        """float: 'AssumedMaximumPinionTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssumedMaximumPinionTorque

        if temp is None:
            return None

        return temp

    @property
    def contact_ellipse_width_instantaneous(self) -> 'float':
        """float: 'ContactEllipseWidthInstantaneous' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactEllipseWidthInstantaneous

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_g(self) -> 'float':
        """float: 'GeometryFactorG' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorG

        if temp is None:
            return None

        return temp

    @property
    def load_factor_scoring(self) -> 'float':
        """float: 'LoadFactorScoring' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorScoring

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
    def safety_factor_scoring(self) -> 'float':
        """float: 'SafetyFactorScoring' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorScoring

        if temp is None:
            return None

        return temp

    @property
    def scoring_factor(self) -> 'float':
        """float: 'ScoringFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScoringFactor

        if temp is None:
            return None

        return temp

    @property
    def temperature_rise_at_critical_point_of_contact(self) -> 'float':
        """float: 'TemperatureRiseAtCriticalPointOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TemperatureRiseAtCriticalPointOfContact

        if temp is None:
            return None

        return temp

    @property
    def thermal_factor(self) -> 'float':
        """float: 'ThermalFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalFactor

        if temp is None:
            return None

        return temp

    @property
    def gear_single_flank_ratings(self) -> 'List[_525.GleasonSpiralBevelGearSingleFlankRating]':
        """List[GleasonSpiralBevelGearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gleason_bevel_gear_single_flank_ratings(self) -> 'List[_525.GleasonSpiralBevelGearSingleFlankRating]':
        """List[GleasonSpiralBevelGearSingleFlankRating]: 'GleasonBevelGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonBevelGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
