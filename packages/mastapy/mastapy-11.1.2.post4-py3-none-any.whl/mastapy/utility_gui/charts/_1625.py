"""_1625.py

BubbleChartDefinition
"""


from mastapy.utility_gui.charts import _1631
from mastapy._internal.python_net import python_net_import

_BUBBLE_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'BubbleChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('BubbleChartDefinition',)


class BubbleChartDefinition(_1631.ScatterChartDefinition):
    """BubbleChartDefinition

    This is a mastapy class.
    """

    TYPE = _BUBBLE_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'BubbleChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
