"""_22.py

ShaftGroove
"""


from mastapy._internal import constructor
from mastapy.shafts import _39, _21
from mastapy._internal.python_net import python_net_import

_SHAFT_GROOVE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftGroove')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftGroove',)


class ShaftGroove(_21.ShaftFeature):
    """ShaftGroove

    This is a mastapy class.
    """

    TYPE = _SHAFT_GROOVE

    def __init__(self, instance_to_wrap: 'ShaftGroove.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def depth(self) -> 'float':
        """float: 'Depth' is the original name of this property."""

        temp = self.wrapped.Depth

        if temp is None:
            return None

        return temp

    @depth.setter
    def depth(self, value: 'float'):
        self.wrapped.Depth = float(value) if value else 0.0

    @property
    def fillet_radius(self) -> 'float':
        """float: 'FilletRadius' is the original name of this property."""

        temp = self.wrapped.FilletRadius

        if temp is None:
            return None

        return temp

    @fillet_radius.setter
    def fillet_radius(self, value: 'float'):
        self.wrapped.FilletRadius = float(value) if value else 0.0

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

    def add_new_groove(self):
        """ 'AddNewGroove' is the original name of this method."""

        self.wrapped.AddNewGroove()
