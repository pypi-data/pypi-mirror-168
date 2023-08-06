"""_1474.py

MomentOfInertiaPerUnitLength
"""


from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_MOMENT_OF_INERTIA_PER_UNIT_LENGTH = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'MomentOfInertiaPerUnitLength')


__docformat__ = 'restructuredtext en'
__all__ = ('MomentOfInertiaPerUnitLength',)


class MomentOfInertiaPerUnitLength(_1406.MeasurementBase):
    """MomentOfInertiaPerUnitLength

    This is a mastapy class.
    """

    TYPE = _MOMENT_OF_INERTIA_PER_UNIT_LENGTH

    def __init__(self, instance_to_wrap: 'MomentOfInertiaPerUnitLength.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
