"""_1030.py

RootStressSurfaceChartOption
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROOT_STRESS_SURFACE_CHART_OPTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'RootStressSurfaceChartOption')


__docformat__ = 'restructuredtext en'
__all__ = ('RootStressSurfaceChartOption',)


class RootStressSurfaceChartOption(Enum):
    """RootStressSurfaceChartOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _ROOT_STRESS_SURFACE_CHART_OPTION

    DISTANCE_ALONG_FILLET = 0
    DIAMETER = 1
    RADIUS = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


RootStressSurfaceChartOption.__setattr__ = __enum_setattr
RootStressSurfaceChartOption.__delattr__ = __enum_delattr
