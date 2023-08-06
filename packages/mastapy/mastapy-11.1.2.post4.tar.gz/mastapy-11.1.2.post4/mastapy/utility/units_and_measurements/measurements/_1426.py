"""_1426.py

Damage
"""


from mastapy.utility.units_and_measurements.measurements import _1441
from mastapy._internal.python_net import python_net_import

_DAMAGE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Damage')


__docformat__ = 'restructuredtext en'
__all__ = ('Damage',)


class Damage(_1441.FractionMeasurementBase):
    """Damage

    This is a mastapy class.
    """

    TYPE = _DAMAGE

    def __init__(self, instance_to_wrap: 'Damage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
