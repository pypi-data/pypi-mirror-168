"""_1418.py

AngularAcceleration
"""


from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_ANGULAR_ACCELERATION = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'AngularAcceleration')


__docformat__ = 'restructuredtext en'
__all__ = ('AngularAcceleration',)


class AngularAcceleration(_1406.MeasurementBase):
    """AngularAcceleration

    This is a mastapy class.
    """

    TYPE = _ANGULAR_ACCELERATION

    def __init__(self, instance_to_wrap: 'AngularAcceleration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
