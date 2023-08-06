"""_1630.py

ParallelCoordinatesChartDefinition
"""


from mastapy.utility_gui.charts import _1634
from mastapy._internal.python_net import python_net_import

_PARALLEL_COORDINATES_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'ParallelCoordinatesChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('ParallelCoordinatesChartDefinition',)


class ParallelCoordinatesChartDefinition(_1634.TwoDChartDefinition):
    """ParallelCoordinatesChartDefinition

    This is a mastapy class.
    """

    TYPE = _PARALLEL_COORDINATES_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'ParallelCoordinatesChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
