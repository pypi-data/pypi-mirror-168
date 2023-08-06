"""_2207.py

GuideModelUsage
"""


from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GUIDE_MODEL_USAGE = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideModelUsage')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideModelUsage',)


class GuideModelUsage(_0.APIBase):
    """GuideModelUsage

    This is a mastapy class.
    """

    TYPE = _GUIDE_MODEL_USAGE

    def __init__(self, instance_to_wrap: 'GuideModelUsage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def alignment_method(self) -> 'GuideModelUsage.AlignmentOptions':
        """AlignmentOptions: 'AlignmentMethod' is the original name of this property."""

        temp = self.wrapped.AlignmentMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(GuideModelUsage.AlignmentOptions)(value) if value is not None else None

    @alignment_method.setter
    def alignment_method(self, value: 'GuideModelUsage.AlignmentOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def clip_drawing(self) -> 'bool':
        """bool: 'ClipDrawing' is the original name of this property."""

        temp = self.wrapped.ClipDrawing

        if temp is None:
            return None

        return temp

    @clip_drawing.setter
    def clip_drawing(self, value: 'bool'):
        self.wrapped.ClipDrawing = bool(value) if value else False

    @property
    def clipping_bottom(self) -> 'float':
        """float: 'ClippingBottom' is the original name of this property."""

        temp = self.wrapped.ClippingBottom

        if temp is None:
            return None

        return temp

    @clipping_bottom.setter
    def clipping_bottom(self, value: 'float'):
        self.wrapped.ClippingBottom = float(value) if value else 0.0

    @property
    def clipping_left(self) -> 'float':
        """float: 'ClippingLeft' is the original name of this property."""

        temp = self.wrapped.ClippingLeft

        if temp is None:
            return None

        return temp

    @clipping_left.setter
    def clipping_left(self, value: 'float'):
        self.wrapped.ClippingLeft = float(value) if value else 0.0

    @property
    def clipping_right(self) -> 'float':
        """float: 'ClippingRight' is the original name of this property."""

        temp = self.wrapped.ClippingRight

        if temp is None:
            return None

        return temp

    @clipping_right.setter
    def clipping_right(self, value: 'float'):
        self.wrapped.ClippingRight = float(value) if value else 0.0

    @property
    def clipping_top(self) -> 'float':
        """float: 'ClippingTop' is the original name of this property."""

        temp = self.wrapped.ClippingTop

        if temp is None:
            return None

        return temp

    @clipping_top.setter
    def clipping_top(self, value: 'float'):
        self.wrapped.ClippingTop = float(value) if value else 0.0

    @property
    def force_monochrome(self) -> 'bool':
        """bool: 'ForceMonochrome' is the original name of this property."""

        temp = self.wrapped.ForceMonochrome

        if temp is None:
            return None

        return temp

    @force_monochrome.setter
    def force_monochrome(self, value: 'bool'):
        self.wrapped.ForceMonochrome = bool(value) if value else False

    @property
    def layout(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'Layout' is the original name of this property."""

        temp = self.wrapped.Layout

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @layout.setter
    def layout(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.Layout = value

    @property
    def origin_horizontal(self) -> 'float':
        """float: 'OriginHorizontal' is the original name of this property."""

        temp = self.wrapped.OriginHorizontal

        if temp is None:
            return None

        return temp

    @origin_horizontal.setter
    def origin_horizontal(self, value: 'float'):
        self.wrapped.OriginHorizontal = float(value) if value else 0.0

    @property
    def origin_vertical(self) -> 'float':
        """float: 'OriginVertical' is the original name of this property."""

        temp = self.wrapped.OriginVertical

        if temp is None:
            return None

        return temp

    @origin_vertical.setter
    def origin_vertical(self, value: 'float'):
        self.wrapped.OriginVertical = float(value) if value else 0.0

    @property
    def rotation(self) -> 'float':
        """float: 'Rotation' is the original name of this property."""

        temp = self.wrapped.Rotation

        if temp is None:
            return None

        return temp

    @rotation.setter
    def rotation(self, value: 'float'):
        self.wrapped.Rotation = float(value) if value else 0.0
