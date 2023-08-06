"""_528.py

SpiralBevelMeshSingleFlankRating
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.rating.conical import _512
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'SpiralBevelMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelMeshSingleFlankRating',)


class SpiralBevelMeshSingleFlankRating(_512.ConicalMeshSingleFlankRating):
    """SpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'SpiralBevelMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DynamicFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def dynamic_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DynamicFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def elastic_coefficient(self) -> 'float':
        """float: 'ElasticCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticCoefficient

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_i(self) -> 'float':
        """float: 'GeometryFactorI' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorI

        if temp is None:
            return None

        return temp

    @property
    def inertia_factor_contact(self) -> 'float':
        """float: 'InertiaFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InertiaFactorContact

        if temp is None:
            return None

        return temp

    @property
    def length_of_line_of_contact(self) -> 'float':
        """float: 'LengthOfLineOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfLineOfContact

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor_bending(self) -> 'float':
        """float: 'LoadDistributionFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorBending

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor_contact(self) -> 'float':
        """float: 'LoadDistributionFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorContact

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_ratio_contact(self) -> 'float':
        """float: 'LoadSharingRatioContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingRatioContact

        if temp is None:
            return None

        return temp

    @property
    def overload_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OverloadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverloadFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def overload_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OverloadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverloadFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def pitch_line_velocity(self) -> 'float':
        """float: 'PitchLineVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchLineVelocity

        if temp is None:
            return None

        return temp

    @property
    def pitting_resistance_geometry_factor(self) -> 'float':
        """float: 'PittingResistanceGeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PittingResistanceGeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def reliability_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ReliabilityFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReliabilityFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def reliability_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ReliabilityFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReliabilityFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def temperature_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TemperatureFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TemperatureFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def temperature_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TemperatureFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TemperatureFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def transmitted_tangential_load_at_large_end(self) -> 'float':
        """float: 'TransmittedTangentialLoadAtLargeEnd' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmittedTangentialLoadAtLargeEnd

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio(self) -> 'float':
        """float: 'TransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatio

        if temp is None:
            return None

        return temp
