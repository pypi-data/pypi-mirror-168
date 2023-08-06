"""_370.py

StraightBevelDiffGearMeshRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.straight_bevel_diff import _929
from mastapy.gears.rating.straight_bevel_diff import _373, _371
from mastapy.gears.rating.conical import _505
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevelDiff', 'StraightBevelDiffGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshRating',)


class StraightBevelDiffGearMeshRating(_505.ConicalGearMeshRating):
    """StraightBevelDiffGearMeshRating

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def derating_factor(self) -> 'float':
        """float: 'DeratingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeratingFactor

        if temp is None:
            return None

        return temp

    @property
    def inertia_factor_bending(self) -> 'float':
        """float: 'InertiaFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InertiaFactorBending

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor(self) -> 'float':
        """float: 'LoadDistributionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactor

        if temp is None:
            return None

        return temp

    @property
    def rating_result(self) -> 'str':
        """str: 'RatingResult' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingResult

        if temp is None:
            return None

        return temp

    @property
    def straight_bevel_diff_gear_mesh(self) -> '_929.StraightBevelDiffGearMeshDesign':
        """StraightBevelDiffGearMeshDesign: 'StraightBevelDiffGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def meshed_gears(self) -> 'List[_373.StraightBevelDiffMeshedGearRating]':
        """List[StraightBevelDiffMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gears_in_mesh(self) -> 'List[_373.StraightBevelDiffMeshedGearRating]':
        """List[StraightBevelDiffMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearsInMesh

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_ratings(self) -> 'List[_371.StraightBevelDiffGearRating]':
        """List[StraightBevelDiffGearRating]: 'StraightBevelDiffGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
