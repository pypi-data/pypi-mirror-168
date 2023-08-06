"""_410.py

HypoidGearMeshRating
"""


from typing import List

from mastapy.gears.rating.hypoid.standards import _415
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.hypoid import _949
from mastapy.gears.rating.iso_10300 import _397, _396
from mastapy.gears.rating.conical import _511
from mastapy.gears.rating.hypoid import _411
from mastapy.gears.rating.agma_gleason_conical import _531
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshRating',)


class HypoidGearMeshRating(_531.AGMAGleasonConicalGearMeshRating):
    """HypoidGearMeshRating

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'HypoidGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gleason_hypoid_mesh_single_flank_rating(self) -> '_415.GleasonHypoidMeshSingleFlankRating':
        """GleasonHypoidMeshSingleFlankRating: 'GleasonHypoidMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonHypoidMeshSingleFlankRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hypoid_gear_mesh(self) -> '_949.HypoidGearMeshDesign':
        """HypoidGearMeshDesign: 'HypoidGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b1(self) -> '_397.ISO10300MeshSingleFlankRatingMethodB1':
        """ISO10300MeshSingleFlankRatingMethodB1: 'ISO10300HypoidMeshSingleFlankRatingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB1

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b2(self) -> '_396.Iso10300MeshSingleFlankRatingHypoidMethodB2':
        """Iso10300MeshSingleFlankRatingHypoidMethodB2: 'ISO10300HypoidMeshSingleFlankRatingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB2

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def meshed_gears(self) -> 'List[_511.ConicalMeshedGearRating]':
        """List[ConicalMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gears_in_mesh(self) -> 'List[_511.ConicalMeshedGearRating]':
        """List[ConicalMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearsInMesh

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_ratings(self) -> 'List[_411.HypoidGearRating]':
        """List[HypoidGearRating]: 'HypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
