"""_1332.py

RealVector
"""


from mastapy.math_utility import _1331
from mastapy._internal.python_net import python_net_import

_REAL_VECTOR = python_net_import('SMT.MastaAPI.MathUtility', 'RealVector')


__docformat__ = 'restructuredtext en'
__all__ = ('RealVector',)


class RealVector(_1331.RealMatrix):
    """RealVector

    This is a mastapy class.
    """

    TYPE = _REAL_VECTOR

    def __init__(self, instance_to_wrap: 'RealVector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
