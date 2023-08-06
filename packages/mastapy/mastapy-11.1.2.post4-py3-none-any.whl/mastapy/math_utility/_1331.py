"""_1331.py

RealMatrix
"""


from mastapy.math_utility import _1321
from mastapy._internal.python_net import python_net_import

_REAL_MATRIX = python_net_import('SMT.MastaAPI.MathUtility', 'RealMatrix')


__docformat__ = 'restructuredtext en'
__all__ = ('RealMatrix',)


class RealMatrix(_1321.GenericMatrix['float', 'RealMatrix']):
    """RealMatrix

    This is a mastapy class.
    """

    TYPE = _REAL_MATRIX

    def __init__(self, instance_to_wrap: 'RealMatrix.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
