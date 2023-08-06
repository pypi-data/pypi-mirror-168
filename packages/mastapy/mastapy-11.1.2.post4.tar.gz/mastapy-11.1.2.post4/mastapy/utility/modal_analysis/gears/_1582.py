"""_1582.py

OrderSelector
"""


from mastapy.utility.modal_analysis.gears import _1581
from mastapy._internal.python_net import python_net_import

_ORDER_SELECTOR = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'OrderSelector')


__docformat__ = 'restructuredtext en'
__all__ = ('OrderSelector',)


class OrderSelector(_1581.OrderForTE):
    """OrderSelector

    This is a mastapy class.
    """

    TYPE = _ORDER_SELECTOR

    def __init__(self, instance_to_wrap: 'OrderSelector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
