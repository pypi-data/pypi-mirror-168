"""_2366.py

PartDetailConfiguration
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.system_model.part_model import _2218
from mastapy._internal.python_net import python_net_import

_PART_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'PartDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('PartDetailConfiguration',)


TPartDetailSelection = TypeVar('TPartDetailSelection')
TPart = TypeVar('TPart', bound='_2218.Part')
TSelectableItem = TypeVar('TSelectableItem')


class PartDetailConfiguration(_0.APIBase, Generic[TPartDetailSelection, TPart, TSelectableItem]):
    """PartDetailConfiguration

    This is a mastapy class.

    Generic Types:
        TPartDetailSelection
        TPart
        TSelectableItem
    """

    TYPE = _PART_DETAIL_CONFIGURATION

    def __init__(self, instance_to_wrap: 'PartDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def selections(self) -> 'List[TPartDetailSelection]':
        """List[TPartDetailSelection]: 'Selections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Selections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def delete_configuration(self):
        """ 'DeleteConfiguration' is the original name of this method."""

        self.wrapped.DeleteConfiguration()

    def select_configuration(self):
        """ 'SelectConfiguration' is the original name of this method."""

        self.wrapped.SelectConfiguration()
