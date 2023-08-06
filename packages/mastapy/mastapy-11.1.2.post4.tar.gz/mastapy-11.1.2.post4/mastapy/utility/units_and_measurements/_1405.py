"""_1405.py

InverseUnit
"""


from mastapy.utility.units_and_measurements import _1411
from mastapy._internal.python_net import python_net_import

_INVERSE_UNIT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'InverseUnit')


__docformat__ = 'restructuredtext en'
__all__ = ('InverseUnit',)


class InverseUnit(_1411.Unit):
    """InverseUnit

    This is a mastapy class.
    """

    TYPE = _INVERSE_UNIT

    def __init__(self, instance_to_wrap: 'InverseUnit.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
