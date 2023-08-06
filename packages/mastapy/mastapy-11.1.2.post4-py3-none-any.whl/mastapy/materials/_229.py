"""_229.py

FatigueSafetyFactorItem
"""


from mastapy.materials import _230
from mastapy._internal.python_net import python_net_import

_FATIGUE_SAFETY_FACTOR_ITEM = python_net_import('SMT.MastaAPI.Materials', 'FatigueSafetyFactorItem')


__docformat__ = 'restructuredtext en'
__all__ = ('FatigueSafetyFactorItem',)


class FatigueSafetyFactorItem(_230.FatigueSafetyFactorItemBase):
    """FatigueSafetyFactorItem

    This is a mastapy class.
    """

    TYPE = _FATIGUE_SAFETY_FACTOR_ITEM

    def __init__(self, instance_to_wrap: 'FatigueSafetyFactorItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
