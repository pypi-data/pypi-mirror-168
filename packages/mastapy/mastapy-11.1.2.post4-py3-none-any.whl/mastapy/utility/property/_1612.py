"""_1612.py

DeletableCollectionMember
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DELETABLE_COLLECTION_MEMBER = python_net_import('SMT.MastaAPI.Utility.Property', 'DeletableCollectionMember')


__docformat__ = 'restructuredtext en'
__all__ = ('DeletableCollectionMember',)


T = TypeVar('T')


class DeletableCollectionMember(_0.APIBase, Generic[T]):
    """DeletableCollectionMember

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _DELETABLE_COLLECTION_MEMBER

    def __init__(self, instance_to_wrap: 'DeletableCollectionMember.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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

    @property
    def item(self) -> 'T':
        """T: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Item

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()
