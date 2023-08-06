"""_1665.py

BearingConnectionComponent
"""


from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_CONNECTION_COMPONENT = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'BearingConnectionComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingConnectionComponent',)


class BearingConnectionComponent(_0.APIBase):
    """BearingConnectionComponent

    This is a mastapy class.
    """

    TYPE = _BEARING_CONNECTION_COMPONENT

    def __init__(self, instance_to_wrap: 'BearingConnectionComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
