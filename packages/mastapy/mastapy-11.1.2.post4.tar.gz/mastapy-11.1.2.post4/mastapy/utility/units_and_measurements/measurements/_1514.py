"""_1514.py

Velocity
"""


from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_VELOCITY = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Velocity')


__docformat__ = 'restructuredtext en'
__all__ = ('Velocity',)


class Velocity(_1406.MeasurementBase):
    """Velocity

    This is a mastapy class.
    """

    TYPE = _VELOCITY

    def __init__(self, instance_to_wrap: 'Velocity.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
