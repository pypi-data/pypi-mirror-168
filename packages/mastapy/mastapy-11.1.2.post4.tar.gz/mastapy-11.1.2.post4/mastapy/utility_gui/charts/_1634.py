"""_1634.py

TwoDChartDefinition
"""


from mastapy.utility_gui.charts import _1629
from mastapy._internal.python_net import python_net_import

_TWO_D_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'TwoDChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('TwoDChartDefinition',)


class TwoDChartDefinition(_1629.NDChartDefinition):
    """TwoDChartDefinition

    This is a mastapy class.
    """

    TYPE = _TWO_D_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'TwoDChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
