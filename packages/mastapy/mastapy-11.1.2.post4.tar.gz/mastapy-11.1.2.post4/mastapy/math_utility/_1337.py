"""_1337.py

SquareMatrix
"""


from mastapy.math_utility import _1331
from mastapy._internal.python_net import python_net_import

_SQUARE_MATRIX = python_net_import('SMT.MastaAPI.MathUtility', 'SquareMatrix')


__docformat__ = 'restructuredtext en'
__all__ = ('SquareMatrix',)


class SquareMatrix(_1331.RealMatrix):
    """SquareMatrix

    This is a mastapy class.
    """

    TYPE = _SQUARE_MATRIX

    def __init__(self, instance_to_wrap: 'SquareMatrix.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
