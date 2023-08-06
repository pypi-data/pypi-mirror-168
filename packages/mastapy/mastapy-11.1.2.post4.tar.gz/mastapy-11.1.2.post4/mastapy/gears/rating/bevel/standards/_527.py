"""_527.py

SpiralBevelGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.conical import _509
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'SpiralBevelGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSingleFlankRating',)


class SpiralBevelGearSingleFlankRating(_509.ConicalGearSingleFlankRating):
    """SpiralBevelGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_strength_geometry_factor(self) -> 'float':
        """float: 'BendingStrengthGeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingStrengthGeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def damage_bending(self) -> 'float':
        """float: 'DamageBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DamageBending

        if temp is None:
            return None

        return temp

    @property
    def damage_contact(self) -> 'float':
        """float: 'DamageContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DamageContact

        if temp is None:
            return None

        return temp

    @property
    def distance_factor(self) -> 'float':
        """float: 'DistanceFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DistanceFactor

        if temp is None:
            return None

        return temp

    @property
    def durability_factor(self) -> 'float':
        """float: 'DurabilityFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DurabilityFactor

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_j(self) -> 'float':
        """float: 'GeometryFactorJ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJ

        if temp is None:
            return None

        return temp

    @property
    def life_factor_bending(self) -> 'float':
        """float: 'LifeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorBending

        if temp is None:
            return None

        return temp

    @property
    def life_factor_contact(self) -> 'float':
        """float: 'LifeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorContact

        if temp is None:
            return None

        return temp

    @property
    def surface_condition_factor(self) -> 'float':
        """float: 'SurfaceConditionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceConditionFactor

        if temp is None:
            return None

        return temp

    @property
    def thermal_constant(self) -> 'float':
        """float: 'ThermalConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalConstant

        if temp is None:
            return None

        return temp
