"""_2234.py

SpecifiedConcentricPartGroupDrawingOrder
"""


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model.part_groups import _2237
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Projections', 'SpecifiedConcentricPartGroupDrawingOrder')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecifiedConcentricPartGroupDrawingOrder',)


class SpecifiedConcentricPartGroupDrawingOrder(_0.APIBase):
    """SpecifiedConcentricPartGroupDrawingOrder

    This is a mastapy class.
    """

    TYPE = _SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER

    def __init__(self, instance_to_wrap: 'SpecifiedConcentricPartGroupDrawingOrder.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def concentric_group(self) -> 'list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup':
        """list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup: 'ConcentricGroup' is the original name of this property."""

        temp = self.wrapped.ConcentricGroup

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup)(temp) if temp is not None else None

    @concentric_group.setter
    def concentric_group(self, value: 'list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ConcentricGroup = value

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

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()
