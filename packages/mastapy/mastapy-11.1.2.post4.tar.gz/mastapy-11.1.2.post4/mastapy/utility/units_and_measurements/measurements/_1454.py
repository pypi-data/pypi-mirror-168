"""_1454.py

InverseShortTime
"""


from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_INVERSE_SHORT_TIME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'InverseShortTime')


__docformat__ = 'restructuredtext en'
__all__ = ('InverseShortTime',)


class InverseShortTime(_1406.MeasurementBase):
    """InverseShortTime

    This is a mastapy class.
    """

    TYPE = _INVERSE_SHORT_TIME

    def __init__(self, instance_to_wrap: 'InverseShortTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
