"""_1624.py

DataLoggerWithCharts
"""


from mastapy.math_utility.convergence import _1380
from mastapy._internal.python_net import python_net_import

_DATA_LOGGER_WITH_CHARTS = python_net_import('SMT.MastaAPI.UtilityGUI', 'DataLoggerWithCharts')


__docformat__ = 'restructuredtext en'
__all__ = ('DataLoggerWithCharts',)


class DataLoggerWithCharts(_1380.DataLogger):
    """DataLoggerWithCharts

    This is a mastapy class.
    """

    TYPE = _DATA_LOGGER_WITH_CHARTS

    def __init__(self, instance_to_wrap: 'DataLoggerWithCharts.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
