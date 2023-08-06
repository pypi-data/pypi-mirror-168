"""_1631.py

ScatterChartDefinition
"""


from mastapy.utility_gui.charts import _1634
from mastapy._internal.python_net import python_net_import

_SCATTER_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'ScatterChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('ScatterChartDefinition',)


class ScatterChartDefinition(_1634.TwoDChartDefinition):
    """ScatterChartDefinition

    This is a mastapy class.
    """

    TYPE = _SCATTER_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'ScatterChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
