"""_415.py

GleasonHypoidMeshSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.rating.conical import _512
from mastapy._internal.python_net import python_net_import

_GLEASON_HYPOID_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid.Standards', 'GleasonHypoidMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GleasonHypoidMeshSingleFlankRating',)


class GleasonHypoidMeshSingleFlankRating(_512.ConicalMeshSingleFlankRating):
    """GleasonHypoidMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _GLEASON_HYPOID_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'GleasonHypoidMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculated_contact_stress(self) -> 'float':
        """float: 'CalculatedContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedContactStress

        if temp is None:
            return None

        return temp

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
    def size_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SizeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

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
