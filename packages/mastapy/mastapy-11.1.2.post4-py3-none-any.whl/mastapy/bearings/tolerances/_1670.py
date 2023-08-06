"""_1670.py

InnerRingTolerance
"""


from mastapy.bearings.tolerances import _1681
from mastapy._internal.python_net import python_net_import

_INNER_RING_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'InnerRingTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerRingTolerance',)


class InnerRingTolerance(_1681.RingTolerance):
    """InnerRingTolerance

    This is a mastapy class.
    """

    TYPE = _INNER_RING_TOLERANCE

    def __init__(self, instance_to_wrap: 'InnerRingTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
