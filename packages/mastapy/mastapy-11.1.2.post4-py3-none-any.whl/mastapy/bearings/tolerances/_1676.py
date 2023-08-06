"""_1676.py

OuterRingTolerance
"""


from mastapy.bearings.tolerances import _1681
from mastapy._internal.python_net import python_net_import

_OUTER_RING_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'OuterRingTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterRingTolerance',)


class OuterRingTolerance(_1681.RingTolerance):
    """OuterRingTolerance

    This is a mastapy class.
    """

    TYPE = _OUTER_RING_TOLERANCE

    def __init__(self, instance_to_wrap: 'OuterRingTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
