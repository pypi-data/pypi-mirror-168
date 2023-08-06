"""_531.py

AGMAGleasonConicalGearMeshRating
"""


from mastapy.gears.gear_designs.conical import _1123
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.rating.conical import _505
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.AGMAGleasonConical', 'AGMAGleasonConicalGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshRating',)


class AGMAGleasonConicalGearMeshRating(_505.ConicalGearMeshRating):
    """AGMAGleasonConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_distribution_factor_method(self) -> '_1123.LoadDistributionFactorMethods':
        """LoadDistributionFactorMethods: 'LoadDistributionFactorMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1123.LoadDistributionFactorMethods)(value) if value is not None else None

    @property
    def maximum_relative_displacement(self) -> 'float':
        """float: 'MaximumRelativeDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRelativeDisplacement

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
