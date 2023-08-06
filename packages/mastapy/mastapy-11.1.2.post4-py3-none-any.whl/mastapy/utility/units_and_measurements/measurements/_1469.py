"""_1469.py

LinearStiffness
"""


from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_LINEAR_STIFFNESS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'LinearStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('LinearStiffness',)


class LinearStiffness(_1406.MeasurementBase):
    """LinearStiffness

    This is a mastapy class.
    """

    TYPE = _LINEAR_STIFFNESS

    def __init__(self, instance_to_wrap: 'LinearStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
