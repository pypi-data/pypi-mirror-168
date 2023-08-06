"""_1018.py

ISO6336GeometryManufactured
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1016
from mastapy._internal.python_net import python_net_import

_ISO6336_GEOMETRY_MANUFACTURED = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ISO6336GeometryManufactured')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336GeometryManufactured',)


class ISO6336GeometryManufactured(_1016.ISO6336GeometryBase):
    """ISO6336GeometryManufactured

    This is a mastapy class.
    """

    TYPE = _ISO6336_GEOMETRY_MANUFACTURED

    def __init__(self, instance_to_wrap: 'ISO6336GeometryManufactured.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso6336_root_fillet_radius(self) -> 'float':
        """float: 'ISO6336RootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336RootFilletRadius

        if temp is None:
            return None

        return temp

    @property
    def iso6336_tooth_root_chord(self) -> 'float':
        """float: 'ISO6336ToothRootChord' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336ToothRootChord

        if temp is None:
            return None

        return temp
