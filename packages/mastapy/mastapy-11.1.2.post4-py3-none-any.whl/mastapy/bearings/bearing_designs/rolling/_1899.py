"""_1899.py

BallBearingShoulderDefinition
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BALL_BEARING_SHOULDER_DEFINITION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BallBearingShoulderDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('BallBearingShoulderDefinition',)


class BallBearingShoulderDefinition(_0.APIBase):
    """BallBearingShoulderDefinition

    This is a mastapy class.
    """

    TYPE = _BALL_BEARING_SHOULDER_DEFINITION

    def __init__(self, instance_to_wrap: 'BallBearingShoulderDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def chamfer(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Chamfer' is the original name of this property."""

        temp = self.wrapped.Chamfer

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @chamfer.setter
    def chamfer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Chamfer = value

    @property
    def diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Diameter' is the original name of this property."""

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @diameter.setter
    def diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Diameter = value

    @property
    def height(self) -> 'float':
        """float: 'Height' is the original name of this property."""

        temp = self.wrapped.Height

        if temp is None:
            return None

        return temp

    @height.setter
    def height(self, value: 'float'):
        self.wrapped.Height = float(value) if value else 0.0

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp
