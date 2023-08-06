"""_32.py

ShaftRadialHole
"""


from mastapy._internal import constructor
from mastapy.shafts import _39, _21
from mastapy._internal.python_net import python_net_import

_SHAFT_RADIAL_HOLE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftRadialHole')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftRadialHole',)


class ShaftRadialHole(_21.ShaftFeature):
    """ShaftRadialHole

    This is a mastapy class.
    """

    TYPE = _SHAFT_RADIAL_HOLE

    def __init__(self, instance_to_wrap: 'ShaftRadialHole.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle(self) -> 'float':
        """float: 'Angle' is the original name of this property."""

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return temp

    @angle.setter
    def angle(self, value: 'float'):
        self.wrapped.Angle = float(value) if value else 0.0

    @property
    def diameter(self) -> 'float':
        """float: 'Diameter' is the original name of this property."""

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return temp

    @diameter.setter
    def diameter(self, value: 'float'):
        self.wrapped.Diameter = float(value) if value else 0.0

    @property
    def surface_roughness(self) -> '_39.ShaftSurfaceRoughness':
        """ShaftSurfaceRoughness: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceRoughness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def add_new_radial_hole(self):
        """ 'AddNewRadialHole' is the original name of this method."""

        self.wrapped.AddNewRadialHole()
