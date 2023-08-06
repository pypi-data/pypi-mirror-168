"""_935.py

SpiralBevelMeshedGearDesign
"""


from mastapy._math.vector_2d import Vector2D
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.bevel import _1137
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.SpiralBevel', 'SpiralBevelMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelMeshedGearDesign',)


class SpiralBevelMeshedGearDesign(_1137.BevelMeshedGearDesign):
    """SpiralBevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'SpiralBevelMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def tip_point_at_mean_section(self) -> 'Vector2D':
        """Vector2D: 'TipPointAtMeanSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipPointAtMeanSection

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def tip_thickness_at_mean_section(self) -> 'float':
        """float: 'TipThicknessAtMeanSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipThicknessAtMeanSection

        if temp is None:
            return None

        return temp
