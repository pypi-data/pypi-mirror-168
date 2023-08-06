"""_1586.py

UserDefinedOrderForTE
"""


from mastapy.utility.modal_analysis.gears import _1583
from mastapy._internal.python_net import python_net_import

_USER_DEFINED_ORDER_FOR_TE = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'UserDefinedOrderForTE')


__docformat__ = 'restructuredtext en'
__all__ = ('UserDefinedOrderForTE',)


class UserDefinedOrderForTE(_1583.OrderWithRadius):
    """UserDefinedOrderForTE

    This is a mastapy class.
    """

    TYPE = _USER_DEFINED_ORDER_FOR_TE

    def __init__(self, instance_to_wrap: 'UserDefinedOrderForTE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
